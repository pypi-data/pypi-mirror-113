from typing import Dict
import pandas as pd

from .base_interface import BaseInterface
from ...utils import parse_xcom_ipcparam, update_xcom_ipcparam
from .....utils.utils import create_operation, get_conn_db
from .....libs.clients.ceh_resource_client import CehResourse
from .....libs.ipc.parameters.parameters import IPCParams
from .....libs.exceptions.exception import ResourceStateException

from ceh_core_infa.config import (
    WF_NAME_LOAD,
    DB_PARAMS,
    DB_QUERY__DELTA_STATEMENT,
    META_VERSION
)


class UpdateResourceStateInterfaceOld(BaseInterface):
    def __init__(self, wf_id, xcom_data, provide_file_param, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wf_id = wf_id
        self.xcom_data = xcom_data
        self.provide_file_param = provide_file_param

    @staticmethod
    def __get__statement_delta(
            query: str,
            instance_id: int,
            wf_name: str,
            meta_id: int,
            db_param: Dict[str, str],
            logger
    ):
        logger.info('Trying to get delta and statment from greenplum')

        conn = get_conn_db(db_param)

        df = pd.read_sql_query(
            sql=query % (instance_id, wf_name, meta_id),
            con=conn
        )

        if df.shape == (0, 0):
            raise RuntimeError('Failed, no data')

        result = df.to_dict(orient='index')

        logger.info('Data received successfully')

        return result.values()

    @staticmethod
    def __get_current_src_version(resource_cd):
        current_state = CehResourse.get_resourse(resource_cd).state

        if not current_state:
            raise ResourceStateException(f'Source {resource_cd} has no state.')

        return current_state.version.version_id

    @staticmethod
    def generate_file_params(param, tgt_vers_id):
        tmp_param = IPCParams.get_params_load(
            old_param=param['prepare_param'],
            tgt_current_vrs=tgt_vers_id
        )

        result = IPCParams.add_conf_file(
            wf_name=WF_NAME_LOAD,
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

    def provide_file_params_to_xcom(self, xcom_data, tgt_cur_version_id):
        param = self.generate_file_params(
            param=xcom_data[self.wf_id],
            tgt_vers_id=tgt_cur_version_id
        )
        xcom_data[self.wf_id] = param
        self.update_xcom(data=xcom_data)

    def execute(self):
        tgt_resource_cd, tgt_table_name, src_resource_name, instance_id, wf_name, tx_uid, _ = parse_xcom_ipcparam(
            self.xcom_data.value, self.wf_id)

        se = self.static_executor(
            ex_func=self.__get_current_src_version,
            op_kwargs={'resource_cd': src_resource_name, }
        )
        src_version_id = se.executor()

        de = self.dynamic_executor(
            ex_func=self.__get__statement_delta,
            op_kwargs={
                'query': DB_QUERY__DELTA_STATEMENT,
                'instance_id': instance_id,
                'wf_name': wf_name,
                'meta_id': META_VERSION,
                'db_param': DB_PARAMS,
                'logger': self.log
            },
            timer=self.timer
        )
        received_inf = de.executor()

        received_inf = list(received_inf)[0]

        operation = create_operation(
            resource_cd=tgt_resource_cd,
            src_version_id=src_version_id,
            statement=received_inf['o_sql_text'],
            delta=received_inf['o_dlt_name'],
            src_resource_name=src_resource_name,
            tgt_table_name=tgt_table_name
        )

        CehResourse.update_resource_state(
            tgt_resource_cd,
            operation,
            tx_uid
        )

        tgt_cur_version_id = CehResourse.get_resourse(
            tgt_resource_cd
        ).state.version.version_id

        xcom_data = self.xcom_data.value

        if self.provide_file_param:
            self.provide_file_params_to_xcom(
                xcom_data=xcom_data,
                tgt_cur_version_id=tgt_cur_version_id
            )

        self.log.info('Success')


class UpdateResourceStateInterface(BaseInterface):
    def __init__(self, global_data, slw_wf_name, provide_file_param, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slw_wf_name = slw_wf_name
        self.global_data = global_data
        self.provide_file_param = provide_file_param
        self.current_ipc_param = None

    @staticmethod
    def __get__statement_delta(
            query: str,
            instance_id: int,
            wf_name: str,
            meta_id: int,
            db_param: Dict[str, str],
            logger
    ):
        logger.info('Trying to get delta and statment from greenplum')

        conn = get_conn_db(db_param)

        df = pd.read_sql_query(
            sql=query % (instance_id, wf_name, meta_id),
            con=conn
        )

        if df.shape == (0, 0):
            raise RuntimeError('Failed, no data')

        result = df.to_dict(orient='index')

        logger.info('Data received successfully')

        return result.values()

    @staticmethod
    def __get_current_src_version(resource_cd):
        current_state = CehResourse.get_resourse(resource_cd).state

        if not current_state:
            raise ResourceStateException(f'Source {resource_cd} has no state.')

        return current_state.version.version_id

    @staticmethod
    def generate_file_params(param, tgt_vers_id):
        tmp_param = IPCParams.get_params_load(
            old_param=param['wf_params']['prepare_param'],
            tgt_current_vrs=tgt_vers_id
        )

        result = IPCParams.add_conf_file(
            wf_name=WF_NAME_LOAD,
            params=tmp_param,
            folder=param['wf_params']['prepare_param']['folder'],
            template_name='ipc_pattern_load.PARAM',
            prefix='param_path'
        )

        param['wf_params']['load_param'] = result

        return param

    def update_xcom(self, data):
        update_xcom_ipcparam(
            key=self.global_data.key,
            value=data,
            task_id=self.global_data.task_id,
            dag_id=self.global_data.dag_id,
            execution_date=self.global_data.execution_date
        )

    def provide_file_params_to_xcom(self, xcom_data, tgt_cur_version_id):
        self.current_ipc_param = self.generate_file_params(
            param=xcom_data['workflows'][self.slw_wf_name],
            tgt_vers_id=tgt_cur_version_id
        )

        xcom_data['workflows'][self.slw_wf_name] = self.current_ipc_param

        self.update_xcom(data=xcom_data)

    def __get_max_source_version(self, resources):
        list_res_vrs = [
            self.__get_current_src_version(resource['src_resource_name']) for resource in resources
        ]

        return max(list_res_vrs)

    def execute(self):
        map = self.global_data.value['workflows'][self.slw_wf_name]

        se = self.static_executor(
            ex_func=self.__get_max_source_version,
            op_kwargs={'resources': map['resources'].values(), }
        )

        src_version_id = se.executor()

        de = self.dynamic_executor(
            ex_func=self.__get__statement_delta,
            op_kwargs={
                'query': DB_QUERY__DELTA_STATEMENT,
                'instance_id': map['wf_params']['prepare_param']['INSTANCE_ID'],
                'wf_name': self.slw_wf_name,
                'meta_id': META_VERSION,
                'db_param': DB_PARAMS,
                'logger': self.log
            },
            timer=self.timer
        )
        received_inf = de.executor()

        received_inf = list(received_inf)[0]
        for key, value in map['resources'].items():
            operation = create_operation(
                resource_cd=value['tgt_resource_name'],
                src_version_id=src_version_id,
                statement=received_inf['o_sql_text'],
                delta=received_inf['o_dlt_name'],
                src_resource_name=value['src_resource_name'],
                tgt_table_name=value['tgt_table_name']
            )

            CehResourse.update_resource_state(
                resource_cd=value['tgt_resource_name'],
                operation=operation,
                tx_uid=self.global_data.value['tx_info']['tx_uid']
            )

            tgt_cur_version_id = CehResourse.get_resourse(
                value['tgt_resource_name']
            ).state.version.version_id

            xcom_data = self.global_data.value

            if self.provide_file_param:
                if not self.current_ipc_param:
                    self.provide_file_params_to_xcom(
                        xcom_data=xcom_data,
                        tgt_cur_version_id=tgt_cur_version_id
                    )

        self.log.info('Success')
