from abc import ABCMeta, abstractmethod
from typing import Dict

from airflow.utils.log.logging_mixin import LoggingMixin
from .....utils.executor import StaticExecutor, DynamicExecutor


class BaseInterface(LoggingMixin, metaclass=ABCMeta):
    def __init__(
            self,
            timer: Dict[str, int] = {},
            static_execute: StaticExecutor = None,
            dynamic_executor: DynamicExecutor = None
    ):
        self.static_executor = static_execute or StaticExecutor
        self.dynamic_executor = dynamic_executor or DynamicExecutor
        self.timer = timer

    @abstractmethod
    def execute(self):
        raise NotImplementedError(
            'Define a execute in %s.' % self.__class__.__name__
        )
