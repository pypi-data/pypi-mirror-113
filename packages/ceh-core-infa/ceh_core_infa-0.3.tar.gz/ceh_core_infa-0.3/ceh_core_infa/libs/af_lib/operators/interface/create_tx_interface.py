from .base_interface import BaseInterface

from .....libs.clients.transaction_manager_client import TxManager
from ...utils import update_xcom_ipcparam


class CreateTransactionInterfaceOld(BaseInterface):
    def __init__(self, xcom_params, tx_timeout, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xcom_params = xcom_params
        self.tx_timeout = tx_timeout

    @staticmethod
    def create_transaction(xcom_params, tx_timeout, logger, *args, **kwargs):
        tx_info = TxManager.create_transaction(tx_timeout)
        for key, _ in xcom_params.value.items():
            xcom_params.value[key]['tx_info'] = {
                'tx_uid': tx_info.tx_uid,
                'tx_token': tx_info.tx_token
            }
        update_xcom_ipcparam(
            key=xcom_params.key,
            value=xcom_params.value,
            task_id=xcom_params.task_id,
            dag_id=xcom_params.dag_id,
            execution_date=xcom_params.execution_date
        )
        logger.info('Success. A new transaction has been created')

    def execute(self):
        op_kwargs = self.__dict__
        op_kwargs['logger'] = self.log
        executor = self.dynamic_executor(
            ex_func=self.create_transaction,
            op_kwargs=op_kwargs,
            timer=self.timer
        )
        executor.executor()


class CreateTransactionInterface(BaseInterface):
    def __init__(self, xcom_params, tx_timeout, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xcom_params = xcom_params
        self.tx_timeout = tx_timeout

    @staticmethod
    def create_transaction(xcom_params, tx_timeout, logger, *args, **kwargs):
        tx_info = TxManager.create_transaction(tx_timeout)

        xcom_params.value['tx_info'] = {
            'tx_uid': tx_info.tx_uid,
            'tx_token': tx_info.tx_token
        }

        update_xcom_ipcparam(
            key=xcom_params.key,
            value=xcom_params.value,
            task_id=xcom_params.task_id,
            dag_id=xcom_params.dag_id,
            execution_date=xcom_params.execution_date
        )
        logger.info('Success. A new transaction has been created')

    def execute(self):
        op_kwargs = self.__dict__
        op_kwargs['logger'] = self.log
        executor = self.dynamic_executor(
            ex_func=self.create_transaction,
            op_kwargs=op_kwargs,
            timer=self.timer
        )
        executor.executor()