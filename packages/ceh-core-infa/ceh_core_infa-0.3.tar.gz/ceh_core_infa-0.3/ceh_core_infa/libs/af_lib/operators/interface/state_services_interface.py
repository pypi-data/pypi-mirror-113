from typing import Dict, Callable

from .base_interface import BaseInterface

from ....clients.ceh_resource_client import CehResourse
from ....clients.increment_client import Sequence
from ....clients.transaction_manager_client import TxManager

HEALTH_SERVICES_USED: Dict[str, Callable] = {
    'ceh_provider_resource': CehResourse.get_health_service,
    'increment': Sequence.get_health_service,
    'transaction_manager': TxManager.get_health_service,
}


class CheckStateServicesInterface(BaseInterface):
    @staticmethod
    def check_state():
        for res in HEALTH_SERVICES_USED.keys():
            procedure = HEALTH_SERVICES_USED[res]
            procedure()

    def execute(self):
        executor = self.dynamic_executor(
            ex_func=self.check_state,
            timer=self.timer
        )
        executor.executor()
