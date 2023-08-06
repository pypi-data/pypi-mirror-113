from .ceh_base_operator import CehBaseOperator
from .interface.get_resources_service_interface import (
    GetResourcesServiceInterface
)


class GetResourcesServiceOperator(CehBaseOperator):
    def execute(self, context):
        table = context['ti'].xcom_pull(
            key='resources',
            include_prior_dates=True
        )

        cls = GetResourcesServiceInterface(
            table=table,
            timer=self._get_timer_poke()
        )
        cls.execute()
