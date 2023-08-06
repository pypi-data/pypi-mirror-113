from .ceh_base_operator import CehBaseOperator
from .interface.check_block_resource_interface import (
    CheckBlockResourceInterface,
)


class CheckBlockResourceOperator(CehBaseOperator):
    def execute(self, context):
        resources = context['ti'].xcom_pull(
            key='resources',
            include_prior_dates=True
        )
        cls = CheckBlockResourceInterface(
            resources=resources,
            timer=self._get_timer_poke()
        )
        cls.execute()
