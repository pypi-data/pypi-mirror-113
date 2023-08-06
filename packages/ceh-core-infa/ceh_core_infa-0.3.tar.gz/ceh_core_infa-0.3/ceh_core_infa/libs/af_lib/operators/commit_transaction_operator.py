from typing import Dict, List

from airflow.utils.decorators import apply_defaults
from airflow.models.xcom import XCom

from .ceh_base_operator import CehBaseOperator
from .interface.commit_transaction_interface import (
    CommitTransactionInterfaceOld,
    CommitTransactionInterface
)


class CommitTransactionOperatorOld(CehBaseOperator):
    @apply_defaults
    def __init__(
            self,
            xcom_params: XCom,
            error_if_locked: bool = False,
            *args,
            **kwargs) -> None:
        super(CommitTransactionOperatorOld, self).__init__(*args, **kwargs)

        self.xcom_params = xcom_params
        self.error_if_locked = error_if_locked

    def execute(self, context):
        cls = CommitTransactionInterfaceOld(
            self.xcom_params,
            self.error_if_locked
        )
        cls.execute()


class CommitTransactionOperator(CehBaseOperator):
    @apply_defaults
    def __init__(
            self,
            tx_info: Dict,
            resources: List = None,
            error_if_locked: bool = False,
            *args,
            **kwargs) -> None:
        super(CommitTransactionOperator, self).__init__(*args, **kwargs)

        self.tx_info = tx_info
        self.error_if_locked = error_if_locked
        print(resources)
        self.resources = resources

    def execute(self, context):
        cls = CommitTransactionInterface(
            self.tx_info,
            self.resources,
            self.error_if_locked,
        )
        cls.execute()
