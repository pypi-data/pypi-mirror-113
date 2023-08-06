import logging

from typing import Tuple

from .base_dag_builder import BaseDagBuilder
from ...af_lib.operators.check_state_services_operator import CheckStateServicesOperator
from ...af_lib.operators.get_resources_db_operator import GetResourcesDBOperator
from ...af_lib.operators.get_resources_service_operator import GetResourcesServiceOperator
from ...af_lib.operators.check_block_resource_operator import CheckBlockResourceOperator
from ...af_lib.operators.check_version_resource_operator import CheckVersionResourceOperator
from ....config import DB_QUERY_RESOURCES, LOAD_TYPE_CD, META_VERSION


class ControlDagBuilder(BaseDagBuilder):
    """
    Универсальный сборщик упраляющего мехагнизма

    :param workflows: Кортеж содержащий наименование необходимых потоков для загрузки
    :type workflows: Tuple[str, ...]
    """
    def __init__(
            self,
            workflows: Tuple[str, ...],
            **kwargs
    ):
        super().__init__(**kwargs)
        self.workflows = workflows

    def build(self):
        logging.debug(f'Начинаю строить даг {self.dag_name}')
        dag = self._create_dag()

        check_status_services = CheckStateServicesOperator(
            dag=dag,
            task_id="check_status_services",
            attempts=3,
            timeout=10
        )

        get_resource_from_db = GetResourcesDBOperator(
            dag=dag,
            task_id="get_resource_from_db",
            query=DB_QUERY_RESOURCES,
            load_type_cd=LOAD_TYPE_CD[0],
            meta_version=META_VERSION,
            workflows=self.workflows,
            attempts=1,
            timeout=5
        )

        get_ceh_provider_resources = GetResourcesServiceOperator(
            dag=dag,
            task_id="get_resources_from_ceh_resource",
        )

        check_resource_block = CheckBlockResourceOperator(
            dag=dag,
            task_id="resource_lock_check",
            attempts=10,
            timeout=5
        )

        provide_resource_data = CheckVersionResourceOperator(
            dag=dag,
            task_id="provide_resource_data",
            workflows=self.workflows,
            attempts=1,
            timeout=5
        )

        logging.debug(f'Даг {self.dag_name} успешно построент')

        check_status_services >> get_resource_from_db
        get_resource_from_db >> get_ceh_provider_resources
        get_ceh_provider_resources >> check_resource_block
        check_resource_block >> provide_resource_data

        return dag
