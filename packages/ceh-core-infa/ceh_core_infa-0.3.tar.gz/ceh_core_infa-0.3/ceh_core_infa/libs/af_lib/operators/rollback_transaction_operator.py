from typing import Dict, List

from airflow.utils.decorators import apply_defaults
from airflow.models.xcom import XCom

from .ceh_base_operator import CehBaseOperator
from .interface.rollback_transaction_interface import (
    RollbackTransactionInterfaceOld,
    RollbackTransactionInterface
)


class RollbackTransactionOperatorOld(CehBaseOperator):
    @apply_defaults
    def __init__(
            self,
            xcom_params: XCom,
            error_if_locked: bool = False,
            *args,
            **kwargs) -> None:
        super(RollbackTransactionOperatorOld, self).__init__(*args, **kwargs)

        self.xcom_params = xcom_params
        self.error_if_locked = error_if_locked

    def execute(self, context):
        cls = RollbackTransactionInterfaceOld(
            self.xcom_params,
            self.error_if_locked
        )
        cls.execute()


class RollbackTransactionOperator(CehBaseOperator):
    @apply_defaults
    def __init__(
            self,
            tx_info: Dict,
            resources: List = None,
            error_if_locked: bool = False,
            *args,
            **kwargs) -> None:
        super(RollbackTransactionOperator, self).__init__(*args, **kwargs)

        self.tx_info = tx_info
        self.error_if_locked = error_if_locked
        self.resources = resources

    def execute(self, context):
        cls = RollbackTransactionInterface(
            self.tx_info,
            self.resources,
            self.error_if_locked
        )
        cls.execute()
