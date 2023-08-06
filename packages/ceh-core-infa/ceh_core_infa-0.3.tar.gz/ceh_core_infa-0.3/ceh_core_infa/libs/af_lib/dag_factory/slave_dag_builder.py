import logging

from airflow.operators.dummy_operator import DummyOperator

from .base_dag_builder import BaseDagBuilder
from .utils import (
    generate_locked_resources_task,
    generate_task_update_state,
    generate_ipc_task,
    generate_open_tx_task,
    generate_commit_tx_task,
    generate_rollback_tx_task,
    generate_check_block_resources_task

)
from ....config import WF_NAME_PRP, WF_NAME_LOAD
from ..utils import get_xcom_ipcparam


class SlaveDagBuilder(BaseDagBuilder):
    """
        Универсальный сборщик рабочего потока
        :param cf_name: имя управляющего механизма
        :type workflows: Tuple[str, ...]
        :param main_wf_name: имя необходимого потока для загрузки
        :type main_wf_name: str
        """
    def __init__(self, cf_name: str, main_wf_name: str, **kwargs):
        super().__init__(**kwargs)

        self.cf_name = cf_name
        self.main_wf_name = main_wf_name
        self.global_params = None

    def __provide_global_params(self, main_wf_name: str, main_dag_name: str):
        self.global_params = get_xcom_ipcparam(
            dag_id=main_dag_name,
            key=main_wf_name
        )

    def __get_slave_wfs(self):
        tmp = set(self.global_params.value['workflows'].keys())

        return tmp

    def __get_all_tgt_resource(self):
        tmp = set()

        for _, value in self.global_params.value['workflows'].items():
            tmp |= set(
                map(lambda x: x['tgt_resource_name'], value['resources'].values())
            )

        return tmp

    def build(self):
        logging.debug(f'Начинаю строить даг {self.dag_name}')
        dag = self._create_dag()

        self.__provide_global_params(
            main_wf_name=self.main_wf_name,
            main_dag_name=self.cf_name
        )

        if not self.global_params:
            logging.warning('Нет параметров для постронения дага.')
            DummyOperator(task_id=self.main_wf_name, dag=dag)

            return dag
        else:
            main_task = DummyOperator(task_id=self.main_wf_name, dag=dag)

        slv_wf_names = self.__get_slave_wfs()

        open_tx = generate_open_tx_task(
            dag=dag,
            global_params=self.global_params,
        )

        commit = generate_commit_tx_task(
            dag=dag,
            tx_info=self.global_params.value.get('tx_info', None),
            resources=self.__get_all_tgt_resource(),
        )

        rollback = generate_rollback_tx_task(
            dag=dag,
            tx_info=self.global_params.value.get('tx_info', None),
            resources=self.__get_all_tgt_resource(),
        )

        for slv_name in slv_wf_names:
            child_task = DummyOperator(task_id=slv_name, dag=dag)
            prepare_wf = generate_ipc_task(
                dag=dag,
                tsk_id='workflow_prepare_data',
                raw_params=self.global_params.value['workflows'][slv_name],
                slv_wf_name=slv_name,
                workflow=WF_NAME_PRP,
            )

            self.__provide_global_params(
                main_wf_name=self.main_wf_name,
                main_dag_name=self.cf_name
            )

            check_block_resources = generate_check_block_resources_task(
                dag=dag,
                slv_wf_name=slv_name,
                resources=self.global_params.value['workflows'][slv_name]['resources']
            )

            block_resources = generate_locked_resources_task(
                dag=dag,
                slv_wf_name=slv_name,
                resources=self.global_params.value['workflows'][slv_name]['resources'],
                tx_info=self.global_params.value.get('tx_info', None)
            )

            update_state = generate_task_update_state(
                dag=dag,
                global_params=self.global_params,
                slv_wf_name=slv_name
            )

            self.__provide_global_params(
                main_wf_name=self.main_wf_name,
                main_dag_name=self.cf_name
            )

            load_wf = generate_ipc_task(
                dag=dag,
                tsk_id='workflow_load_data',
                raw_params=self.global_params.value['workflows'][slv_name],
                slv_wf_name=slv_name,
                workflow=WF_NAME_LOAD,
                prefix='load_param'
            )

            main_task >> child_task >> prepare_wf >> open_tx
            open_tx >> check_block_resources >> block_resources
            block_resources >> update_state >> load_wf >> commit
            block_resources >> update_state >> load_wf >> rollback

        logging.debug(f'Даг {self.dag_name} успешно построент')

        return dag
