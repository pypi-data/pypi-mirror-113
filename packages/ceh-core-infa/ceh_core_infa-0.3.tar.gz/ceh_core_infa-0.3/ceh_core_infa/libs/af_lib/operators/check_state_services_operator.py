from .ceh_base_operator import CehBaseOperator
from .interface.state_services_interface import CheckStateServicesInterface


class CheckStateServicesOperator(CehBaseOperator):
    def execute(self, context):
        cls = CheckStateServicesInterface(timer=self._get_timer_poke())
        cls.execute()
