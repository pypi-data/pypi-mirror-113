from abc import ABCMeta, abstractmethod

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from ....utils.descriptors.descriptors import ValidateAttempts, ValidateTimeout

from ceh_core_infa.config import (
    ATTEMPS_DAG_CONF,
    TIMEOUT_DAG_CONF,
)


class CehBaseOperator(BaseOperator, metaclass=ABCMeta):
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
        super(CehBaseOperator, self).__init__(*args, **kwargs)
        self.attempts = attempts
        self.timeout = timeout

    def _get_timer_poke(self):
        return {'attempts': self.attempts, 'timeout': self.timeout}

    @abstractmethod
    def execute(self, context):
        raise NotImplementedError(
            'Define a execute in %s.' % self.__class__.__name__
        )
