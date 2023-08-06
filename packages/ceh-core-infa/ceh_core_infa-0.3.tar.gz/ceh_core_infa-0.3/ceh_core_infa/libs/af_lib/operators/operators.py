import time

import pandas as pd
import psycopg2

from typing import Dict, Callable

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException
from airflow.models.xcom import XCom

from ceh_core_infa.config import (
    DB_PARAMS,
    ATTEMPS_DAG_CONF,
    TIMEOUT_DAG_CONF,
    ENVIRONMENT,
    TX_TIMEOUT,
    WF_NAME_LOAD
)

from ....libs.clients.ceh_resource_client import CehResourse
from ....libs.clients.transaction_manager_client import TxManager
from ....libs.clients.increment_client import Sequence
from ....libs.exceptions.exception import (
    ResourceNotFound,
    NumberAttemptsOver,
    SomeVersionException,
    ResourceStateException,
    NotValidStatusCode
)
from ....libs.ipc.exceptions.exceptions import IPCException, BashException
from ....libs.ipc.wf_launcher import IPCLauncher
from ....libs.ipc.parameters.parameters import IPCParams
from ....utils.descriptors.descriptors import ValidateAttempts, ValidateTimeout
from ....utils.version import VersionOld
from ....utils.utils import create_operation
from ..utils import update_xcom_ipcparam, parse_xcom_ipcparam


HEALTH_SERVICES_USED: Dict[str, Callable] = {
    'ceh_provider_resource': CehResourse.get_health_service,
    'increment': Sequence.get_health_service,
    'transaction_manager': TxManager.get_health_service,
}


class CheckStateServicesOperatorOld(BaseOperator):  # old stable operator
    attempts = ValidateAttempts()
    timeout = ValidateTimeout()

    @apply_defaults
    def __init__(
            self,
            attempts: int = ATTEMPS_DAG_CONF,
            timeout: int = TIMEOUT_DAG_CONF,
            *args,
            **kwargs
    ):
        super(CheckStateServicesOperatorOld, self).__init__(*args, **kwargs)
        self.attempts = attempts
        self.timeout = timeout

    def execute(self, context):
        attempt = 1
        while True:
            if attempt > self.attempts:
                raise NumberAttemptsOver('Number of attempts is over.')

            errors = 0
            for res in HEALTH_SERVICES_USED.keys():
                try:
                    procedure = HEALTH_SERVICES_USED[res]
                    procedure()
                except:
                    errors += 1
                    self.log.error(f'The Service {res} not available.')
                    break

            if errors == 0:
                break

            attempt += 1
            if self.attempts > 1:
                time.sleep(self.timeout)


class GetResourcesDBOperatorOld(BaseOperator):  # old stable operator
    attempts = ValidateAttempts()
    timeout = ValidateTimeout()

    @apply_defaults
    def __init__(
            self,
            query: str,
            load_type_cd: str,
            meta_version: str,
            attempts: int = ATTEMPS_DAG_CONF,
            timeout: int = TIMEOUT_DAG_CONF,
            *args,
            **kwargs
    ):
        super(GetResourcesDBOperatorOld, self).__init__(*args, **kwargs)
        self.query = query
        self.load_type_cd = load_type_cd
        self.meta_version = meta_version
        self.attempts = attempts
        self.timeout = timeout

    @staticmethod
    def __connect_db():
        return psycopg2.connect(**DB_PARAMS)

    def __get_mapping_from_db(self):
        conn = self.__connect_db()

        df = pd.read_sql_query(
            sql=self.query % (self.load_type_cd, self.meta_version),
            con=conn
        )

        conn.close()

        if df.shape == (0, 0):
            raise RuntimeError('Failed, no data')

        result = df.to_dict(orient='index')

        return result.values()

    def execute(self, context):
        data = None

        for attempt in range(self.attempts):
            try:
                data = self.__get_mapping_from_db()
                break
            except (ValueError, RuntimeError) as err:
                self.log.error(
                    f'{err} \n'
                    f'Attempt {attempt + 1} of {self.attempts}')
                time.sleep(self.timeout)
                continue
            except:
                self.log.error(
                    f'Error while retrieving data from the database. '
                    f'Attempt {attempt + 1} of {self.attempts}')
                time.sleep(self.timeout)
                continue

        if data is None:
            raise AirflowException(
                'Data retrieval error, maximum number of attempts has been reached'
            )

        context['ti'].xcom_push(key='resources', value=list(data))


class GetResourcesServicesOperatorOld(BaseOperator):
    @apply_defaults
    def __init__(self, *args, **kwargs):
        super(GetResourcesServicesOperatorOld, self).__init__(*args, **kwargs)

    @staticmethod
    def __get_resources():
        return CehResourse.get_resources()

    def __check_resources_srv(self):
        errors = 0

        for resource in self.table:
            target = resource['src_resource_name']
            if target not in self.resources:
                errors += 1
                self.log.error(
                    f'Service {resource} not found in CEH Resource Provider.'
                )

            source = resource['tgt_resource_name']
            if source not in self.resources:
                errors += 1
                self.log.error(
                    f'Service {source} not found in CEH Resource Provider.'
                )

        if errors > 0:
            raise ResourceNotFound(
                f'Services not found in CEH Resource Provider.'
            )

    def execute(self, context):
        self.log.info(
            'Searching for resources in the api.'
        )
        self.table = context['ti'].xcom_pull(key='resources', include_prior_dates=True)
        self.resources = self.__get_resources()
        self.log.info('Successfully. All resources have been found.')
        self.__check_resources_srv()


class CheckBlockResourceOperatorOld(BaseOperator):
    attempts = ValidateAttempts()
    timeout = ValidateTimeout()

    @apply_defaults
    def __init__(
            self,
            attempts: int = ATTEMPS_DAG_CONF,
            timeout: int = TIMEOUT_DAG_CONF,
            *args,
            **kwargs
    ):
        super(CheckBlockResourceOperatorOld, self).__init__(*args, **kwargs)
        self.attempts = attempts
        self.timeout = timeout

    @staticmethod
    def __check_block(resource):
        return CehResourse.get_resourse(resource).is_readonly

    def execute(self, context):
        self.log.info('Checking the required resources for blocking.')
        resources = context['ti'].xcom_pull(key='resources', include_prior_dates=True)

        attempt = 1

        while True:
            if attempt > self.attempts:
                raise NumberAttemptsOver('Number of attempts is over.')

            self.log.info(f'Attempt {attempt} of {self.attempts}')
            errors = 0

            for resource in resources:
                tgt = resource['tgt_resource_name']
                if not self.__check_block(tgt):
                    self.log.info(f'The resource {tgt} is available.')
                else:
                    errors += 1
                    self.log.error(f'The resource {tgt} is locked.')

            if errors == 0:
                break

            attempt += 1
            time.sleep(self.timeout)

        self.log.info('Successfully. All resources are free. Begin.')


class CheckVersionResourceOperator(BaseOperator):
    attempts = ValidateAttempts()
    timeout = ValidateTimeout()

    @apply_defaults
    def __init__(
            self,
            attempts: int = ATTEMPS_DAG_CONF,
            timeout: int = TIMEOUT_DAG_CONF,
            *args,
            **kwargs
    ):
        super(CheckVersionResourceOperator, self).__init__(*args, **kwargs)
        self.attempts = attempts
        self.timeout = timeout

    def __poke(self, resources):
        attempt = 1

        while True:
            if attempt > self.attempts:
                raise NumberAttemptsOver('Number of attempts is over.')

            self.log.info(f'Attempt {attempt} of {self.attempts}')

            try:
                vrs = VersionOld(
                    resources=resources,
                    param_file_create=True
                )
                vrs.check_version()
                params_streams = vrs.params_for_streams
            except SomeVersionException as err:
                self.log.error(err)
            except ResourceStateException as err:
                self.log.error(err)
            else:
                return params_streams
            finally:
                attempt += 1
                time.sleep(self.timeout)

    def execute(self, context):
        resources = context['ti'].xcom_pull(key='resources', include_prior_dates=True)

        params = self.__poke(resources)

        context['ti'].xcom_push(key='ipc_params', value=params)


class IPCLaunchOperator(BaseOperator):
    attempts = ValidateAttempts()
    timeout = ValidateTimeout()

    @apply_defaults
    def __init__(
            self,
            attempts: int = ATTEMPS_DAG_CONF,
            timeout: int = TIMEOUT_DAG_CONF,
            ipc_params: Dict[str, str] = None,
            debug_mode: bool = False,
            *args,
            **kwargs
    ):
        super(IPCLaunchOperator, self).__init__(*args, **kwargs)
        self.attempts = attempts
        self.timeout = timeout
        self.params = ipc_params
        self.debug_mode = debug_mode

    def __provide_log(self, logs, context):
        self.log.info(
            msg=logs['cmd']
        )

        self.log.info(
            msg=self.__generate_system_logs(logs['log'])
        )

        context['ti'].xcom_push(key='ipc_log', value=logs)

    @staticmethod
    def __generate_logs(log):
        tmp = 'Run id %s workflow %s status %s' % (
            log['run_id'],
            log['workflow'],
            log['status'],
        )

        return tmp

    @staticmethod
    def __generate_system_logs(raw_log):
        logs = ''
        for elem in raw_log:
            len_elem = len(elem)
            if len_elem > 1:
                logs += ' '.join(elem)
            else:
                logs += f'{elem[0]} \n'

        return logs

    def __poke(self, context):
        attempt = 1

        while True:
            if attempt > self.attempts:
                raise NumberAttemptsOver('Number of attempts is over.')

            self.log.info(f'Attempt {attempt} of {self.attempts}')

            ipc = IPCLauncher(
                **self.params,
                provide_full_log=self.debug_mode
            )

            try:
                ipc.launch_workflow(ENVIRONMENT)
            except IPCException as err:
                self.log.error(err)
            except BashException as err:
                self.log.error(err)
            except Exception as err:
                self.log.error(err)
            else:
                return ipc.get_system_info()
            finally:
                if self.debug_mode:
                    self.__provide_log(ipc.get_system_info(), context)

                attempt += 1
                time.sleep(self.timeout)

    def execute(self, context):
        if not self.params:
            self.params = context['ti'].xcom_pull(key='ipc_params', include_prior_dates=True)

        logs = self.__poke(context)

        self.log.info(
            msg=self.__generate_logs(logs)
        )

        if self.debug_mode:
            self.__provide_log(logs, context)


class CreateTransactionOperatorOld(BaseOperator):
    attempts = ValidateAttempts()
    timeout = ValidateTimeout()

    @apply_defaults
    def __init__(
            self,
            xcom_params: XCom,
            attempts: int = ATTEMPS_DAG_CONF,
            timeout: int = TIMEOUT_DAG_CONF,
            tx_timeout: int = TX_TIMEOUT,
            *args,
            **kwargs) -> None:
        super(CreateTransactionOperatorOld, self).__init__(*args, **kwargs)

        self.attempts = attempts
        self.timeout = timeout

        self.tx_timeout = tx_timeout

        self.xcom_params = xcom_params

    @staticmethod
    def __create_transaction(tx_timeout):
        return TxManager.create_transaction(tx_timeout)

    def __poke(self):
        attempt = 1

        while True:

            if attempt > self.attempts:
                raise NumberAttemptsOver('Number of attempts is over.')

            self.log.info(f'Attempt {attempt} of {self.attempts}')
            errors = 0

            tx_info = self.__create_transaction(self.tx_timeout)

            if not tx_info:
                errors += 1
                self.log.error(f'Failed to create a new transaction')

            if errors == 0:
                break

            attempt += 1
            time.sleep(self.timeout)

        return tx_info

    def execute(self, context):
        self.log.info('Creating a new transaction')

        tx_info = self.__poke()

        ipc_params = self.xcom_params.value

        for i, v in ipc_params.items():
            ipc_params[i]['tx_info'] = {
                'tx_uid': tx_info.tx_uid,
                'tx_token': tx_info.tx_token
            }

        update_xcom_ipcparam(
            key=self.xcom_params.key,
            value=ipc_params,
            task_id=self.xcom_params.task_id,
            dag_id=self.xcom_params.dag_id,
            execution_date=self.xcom_params.execution_date
        )

        self.log.info('Success. A new transaction has been created')


class UpdateResourceStateOperatorOld(BaseOperator):
    attempts = ValidateAttempts()
    timeout = ValidateTimeout()

    @apply_defaults
    def __init__(
            self,
            wf_id: int,
            xcom_data: XCom,
            provide_file_param: bool = True,
            attempts: int = ATTEMPS_DAG_CONF,
            timeout: int = TIMEOUT_DAG_CONF,
            *args,
            **kwargs) -> None:
        super(UpdateResourceStateOperatorOld, self).__init__(*args, **kwargs)

        self.attempts = attempts
        self.timeout = timeout
        self.wf_id = wf_id
        self.xcom_data = xcom_data
        self.provide_file_param = provide_file_param

    @staticmethod
    def __check_if_locked(resource_cd):
        try:
            resource_state = CehResourse.get_resource_state(resource_cd)

            return resource_state.state.is_locked
        except NotValidStatusCode as err:
            print(f'Resource {resource_cd} is stateless. Error {err}')

            return False

    @staticmethod
    def generate_file_params(param, tgt_vers_id):
        tmp_param = IPCParams.get_params_load(old_param=param['prepare_param'], tgt_current_vrs=tgt_vers_id)

        result = IPCParams.add_conf_file(wf_name=WF_NAME_LOAD,
                                         params=tmp_param,
                                         folder=param['prepare_param']['folder'],
                                         template_name='ipc_pattern_load.PARAM',
                                         prefix='param_path'
                                         )

        param['load_param'] = result

        return param

    def update_xcom(self, data):
        update_xcom_ipcparam(
            key=self.xcom_data.key,
            value=data,
            task_id=self.xcom_data.task_id,
            dag_id=self.xcom_data.dag_id,
            execution_date=self.xcom_data.execution_date
        )

    def __poke(self, resource_cd):
        attempt = 1

        while True:
            if attempt > self.attempts:
                raise NumberAttemptsOver('Number of attempts is over.')

            self.log.info(f'Attempt {attempt} of {self.attempts}')
            errors = 0

            is_locked = self.__check_if_locked(resource_cd)

            if is_locked:
                errors += 1
                self.log.error(f'{resource_cd} is locked')

            if errors == 0:
                break

            attempt += 1
            time.sleep(self.timeout)

    def execute(self, context):
        tgt_resource_cd, tgt_table_name, src_resource_name, tx_uid, tx_token = parse_xcom_ipcparam(
            self.xcom_data.value, self.wf_id)

        self.log.info(f'Checking if {tgt_resource_cd} is locked')

        self.__poke(tgt_resource_cd)
        print(src_resource_name)
        src_version_id = CehResourse.get_resourse(src_resource_name).state.version.version_id

        operation = create_operation(tgt_resource_cd, src_version_id, src_resource_name, tgt_table_name)

        # CehResourse.update_resource_state(tgt_resource_cd, operation, tx_uid)

        tgt_cur_version_id = 1 or CehResourse.get_resourse(tgt_table_name).state.version.version_id
        xcom_data = self.xcom_data.value

        if self.provide_file_param:
            param = self.generate_file_params(param=xcom_data[self.wf_id], tgt_vers_id=tgt_cur_version_id)

            xcom_data[self.wf_id] = param

            self.update_xcom(data=xcom_data)

        self.log.info('Success')
