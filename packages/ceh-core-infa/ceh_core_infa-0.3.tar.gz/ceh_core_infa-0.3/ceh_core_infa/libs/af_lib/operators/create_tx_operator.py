from airflow.utils.decorators import apply_defaults
from airflow.models.xcom import XCom

from .ceh_base_operator import CehBaseOperator
from ....config import (
    TX_TIMEOUT,
)
from .interface.create_tx_interface import (
    CreateTransactionInterface,
)


class CreateTransactionOperatorOld(CehBaseOperator):
    @apply_defaults
    def __init__(
            self,
            xcom_params: XCom,
            tx_timeout: int = TX_TIMEOUT,
            *args,
            **kwargs) -> None:
        super(CreateTransactionOperatorOld, self).__init__(*args, **kwargs)

        self.tx_timeout = tx_timeout
        self.xcom_params = xcom_params

    def execute(self, context):
        cls = CreateTransactionInterface(
            self.xcom_params,
            self.tx_timeout,
            timer=self._get_timer_poke()
        )
        cls.execute()


class CreateTransactionOperator(CehBaseOperator):
    @apply_defaults
    def __init__(
            self,
            xcom_params: XCom,
            tx_timeout: int = TX_TIMEOUT,
            *args,
            **kwargs) -> None:
        super(CreateTransactionOperator, self).__init__(*args, **kwargs)

        self.tx_timeout = tx_timeout
        self.xcom_params = xcom_params

    def execute(self, context):
        cls = CreateTransactionInterface(
            self.xcom_params,
            self.tx_timeout,
            timer=self._get_timer_poke()
        )

        cls.execute()
