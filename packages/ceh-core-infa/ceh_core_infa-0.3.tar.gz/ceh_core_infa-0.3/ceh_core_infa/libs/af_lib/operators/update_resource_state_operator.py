from airflow.utils.decorators import apply_defaults
from airflow.models.xcom import XCom

from .ceh_base_operator import CehBaseOperator
from .interface.update_resource_state_interface import (
    UpdateResourceStateInterfaceOld,
    UpdateResourceStateInterface
)


class UpdateResourceStateOperatorOld(CehBaseOperator):
    @apply_defaults
    def __init__(
            self,
            wf_id: int,
            xcom_data: XCom,
            provide_file_param: bool = True,
            *args,
            **kwargs) -> None:
        super(UpdateResourceStateOperatorOld, self).__init__(*args, **kwargs)

        self.wf_id = wf_id
        self.xcom_data = xcom_data
        self.provide_file_param = provide_file_param

    def execute(self, context):
        cls = UpdateResourceStateInterfaceOld(
            self.wf_id,
            self.xcom_data,
            self.provide_file_param,
            timer=self._get_timer_poke()
        )
        cls.execute()


class UpdateResourceStateOperator(CehBaseOperator):
    @apply_defaults
    def __init__(
            self,
            slw_wf_name: str,
            global_params: XCom,
            provide_file_param: bool = True,
            *args,
            **kwargs) -> None:
        super(UpdateResourceStateOperator, self).__init__(*args, **kwargs)

        self.slw_wf_name = slw_wf_name
        self.global_params = global_params
        self.provide_file_param = provide_file_param

    def execute(self, context):
        cls = UpdateResourceStateInterface(
            slw_wf_name=self.slw_wf_name,
            global_data=self.global_params,
            provide_file_param=self.provide_file_param,
            timer=self._get_timer_poke()
        )
        cls.execute()
