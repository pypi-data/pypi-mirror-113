from typing import Tuple

from airflow.utils.decorators import apply_defaults

from airflow.exceptions import AirflowException

from .ceh_base_operator import CehBaseOperator
from .interface.get_resources_db_interface import GetResourcesDBInterface
from ....config import DB_PARAMS


class GetResourcesDBOperator(CehBaseOperator):
    @apply_defaults
    def __init__(
            self,
            query: str,
            workflows: Tuple[str, ...],
            load_type_cd: str,
            meta_version: str,
            *args,
            **kwargs
    ):
        super(GetResourcesDBOperator, self).__init__(*args, **kwargs)
        self.query = query
        self.load_type_cd = load_type_cd
        self.meta_version = meta_version
        self.workflows = workflows

    def execute(self, context):
        cls = GetResourcesDBInterface(
            db_param=DB_PARAMS,
            meta_version=self.meta_version,
            load_type_cd=self.load_type_cd,
            query=self.query,
            timer=self._get_timer_poke(),
            workflows=self.workflows
            )
        data = cls.execute()

        if data is None:
            raise AirflowException(
                'Data retrieval error, '
                'maximum number of attempts has been reached'
            )

        context['ti'].xcom_push(key='resources', value=list(data))
