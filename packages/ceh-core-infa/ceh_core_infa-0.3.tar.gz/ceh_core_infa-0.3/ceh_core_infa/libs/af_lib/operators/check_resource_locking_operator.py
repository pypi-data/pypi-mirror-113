from typing import Dict

from airflow.utils.decorators import apply_defaults
from airflow.models.xcom import XCom

from .ceh_base_operator import CehBaseOperator
from .interface.check_resource_locking_interface import (
    CheckResourceLockingInterfaceOld,
    CheckResourceLockingInterface
)


class CheckResourceLockingOperatorOld(CehBaseOperator):
    @apply_defaults
    def __init__(
            self,
            xcom_params: XCom,
            *args,
            **kwargs) -> None:
        super(CheckResourceLockingOperatorOld, self).__init__(*args, **kwargs)

        self.xcom_params = xcom_params

    def execute(self, context):
        ex = CheckResourceLockingInterfaceOld(
            xcom_params=self.xcom_params,
            timer=self._get_timer_poke()
        )
        ex.execute()


class CheckResourceLockingOperator(CehBaseOperator):
    @apply_defaults
    def __init__(
            self,
            resources: Dict,
            *args,
            **kwargs) -> None:
        super(CheckResourceLockingOperator, self).__init__(*args, **kwargs)

        self.resources = resources

    def execute(self, context):
        ex = CheckResourceLockingInterface(
            resources=self.resources,
            timer=self._get_timer_poke()
        )
        ex.execute()
