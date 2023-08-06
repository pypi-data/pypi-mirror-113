from typing import Iterable, Dict, Union

from .base_interface import BaseInterface

from .....libs.clients.ceh_resource_client import CehResourse
from .....utils.descriptors.descriptors import IsIterable
from .....utils.utils import check_resource_lock
from .....libs.clients.transaction_manager_client import TxManager
from .....libs.exceptions.exception import (
    ResourceStateException,
    ParamsNotFoundException
)
from ...utils import parse_xcom_ipcparam


class RollbackTransactionInterfaceOld(BaseInterface):
    def __init__(self, xcom_params, error_if_locked, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xcom_params = xcom_params
        self.error_if_locked = error_if_locked

    @staticmethod
    def __check_if_locked(resource_cd, logger):
        logger.info(f'Checking if {resource_cd} is locked')
        resource = CehResourse.get_resourse(resource_cd=resource_cd)

        if not resource.state:
            logger.info(f'Resource {resource_cd} has no state')
            return None

        is_locked = CehResourse.get_resource_state(resource_cd).is_locked

        if is_locked:
            raise ResourceStateException(f'Resource {resource_cd} is locked')

        logger.info(f'Resource {resource_cd} is not locked')

    def rollback_transaction(self, *args, **kwargs):
        wf_id = list(self.xcom_params.value.keys())[0]
        wf_params = self.xcom_params.value.get(wf_id, None)

        if not wf_params:
            raise ParamsNotFoundException('Workflow params not found')
        resource_cd, _, _, _, _, tx_uid, tx_token = parse_xcom_ipcparam(
            self.xcom_params.value,
            wf_id
        )

        TxManager.cancel_transaction(tx_uid, tx_token)

        self.log.info('Transaction has been rolled back')

        return resource_cd

    def execute(self):
        executor = self.static_executor(
            ex_func=self.rollback_transaction,
            op_kwargs=self.__dict__
        )

        resource_cd = executor.executor()

        if self.error_if_locked:
            ex = self.dynamic_executor(
                ex_func=self.__check_if_locked,
                op_kwargs={
                    'resource_cd': resource_cd,
                    'logger': self.log,
                },
                timer=self.timer
            )
            ex.executor()


class RollbackTransactionInterface(BaseInterface):
    resources = IsIterable()

    def __init__(
            self,
            tx_info: Dict[str, Union[str, int]],
            resources: Iterable = None,
            error_if_locked: bool = False,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.tx_info = tx_info
        self.error_if_locked = error_if_locked
        self.resources = resources

    def rollback_transaction(self, *args, **kwargs):
        TxManager.commit_transaction(
            tx_uid=self.tx_info['tx_uid'],
            tx_token=self.tx_info['tx_token']
        )

        self.log.info('Transaction has been rolled back')

    def execute(self):
        se = self.static_executor(
            ex_func=self.rollback_transaction,
        )

        se.executor()

        if self.error_if_locked:
            for resource_cd in self.resources:
                ex = self.dynamic_executor(
                    ex_func=check_resource_lock,
                    op_kwargs={
                        'resource_cd': resource_cd,
                        'logger': self.log,
                    },
                    timer=self.timer
                )
                ex.executor()
