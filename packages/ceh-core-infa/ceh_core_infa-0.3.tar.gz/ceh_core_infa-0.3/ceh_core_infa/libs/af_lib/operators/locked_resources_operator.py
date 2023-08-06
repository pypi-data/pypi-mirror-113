from typing import Dict

from airflow.utils.decorators import apply_defaults
from airflow.models.xcom import XCom

from .ceh_base_operator import CehBaseOperator
from .interface.locked_resources_interface import LockedGroupResourcesInterfaceOld, LockedGroupResourcesInterface


class LockedGroupResourcesOperatorOld(CehBaseOperator):
    @apply_defaults
    def __init__(
            self,
            xcom_params: XCom,
            check_lock: bool = False,
            *args,
            **kwargs) -> None:
        super(LockedGroupResourcesOperatorOld, self).__init__(*args, **kwargs)

        self.xcom_params = xcom_params
        self.check_lock = check_lock

    def execute(self, context):
        inter = LockedGroupResourcesInterfaceOld(
            xcom_data=self.xcom_params,
            check_lock=True,
            timer=self._get_timer_poke()
        )
        inter.execute()


class LockedGroupResourcesOperator(CehBaseOperator):
    @apply_defaults
    def __init__(
            self,
            resources: Dict,
            tx_info: Dict,
            check_lock: bool = False,
            *args,
            **kwargs) -> None:
        super(LockedGroupResourcesOperator, self).__init__(*args, **kwargs)

        self.resources = resources
        self.check_lock = check_lock
        self.tx_info = tx_info

    def execute(self, context):
        inter = LockedGroupResourcesInterface(
            resources=self.resources,
            tx_info=self.tx_info,
            check_lock=self.check_lock,
            timer=self._get_timer_poke()
        )
        inter.execute()
