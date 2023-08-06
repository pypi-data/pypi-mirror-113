import time

from typing import Callable, Optional, List, Dict

from airflow.utils.log.logging_mixin import LoggingMixin

from ..libs.exceptions.exception import NumberAttemptsOver
from ..config import ATTEMPS_DAG_CONF, TIMEOUT_DAG_CONF


class StaticExecutor(LoggingMixin):
    def __init__(
            self,
            ex_func: Callable,
            op_args: Optional[List] = None,
            op_kwargs: Optional[Dict] = None,
    ):
        self.op_args = op_args or list()
        self.op_kwargs = op_kwargs or dict()
        self.ex_func = ex_func

    def executor(self):
        self.log.info('Start execute')

        result = self.execute_callable()

        self.log.info('End execute')

        return result

    def execute_callable(self):
        return self.ex_func(*self.op_args, **self.op_kwargs)


class DynamicExecutor(LoggingMixin):
    def __init__(
            self,
            ex_func: Callable,
            op_args: Optional[List] = None,
            op_kwargs: Optional[Dict] = None,
            attempt: int = ATTEMPS_DAG_CONF,
            timeout: int = TIMEOUT_DAG_CONF,
            timer: Dict[str, int] = {}
    ):
        self.attempts = timer.get('attempts', None) or attempt
        self.timeout = timer.get('timeout', None) or timeout
        self.op_args = op_args or list()
        self.op_kwargs = op_kwargs or dict()
        self.ex_func = ex_func

    def executor(self, attempts: int = None):
        if attempts is None:
            attempts = self.attempts

        if attempts <= 0:
            raise NumberAttemptsOver('Number of attempts is over.')

        try:
            self.log.info(
                f'Start execute. Attempt {self.attempts - (attempts - 1)}.'
            )
            result = self.execute_callable()
        except Exception as err:
            attempts -= 1

            self.log.error(
                f'Attempt {self.attempts - attempts} of {self.attempts}. '
                f'Error: {err} \n'
                )

            time.sleep(self.timeout)

            result = self.executor(attempts)

        return result

    def execute_callable(self):
        return self.ex_func(*self.op_args, **self.op_kwargs)
