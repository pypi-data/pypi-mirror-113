from abc import ABCMeta, abstractmethod

from airflow.utils.dates import days_ago
from airflow.models import DAG

from ....utils.rebuild_domain_ipc import rebuild_domain_ipc


class BaseDagBuilder(metaclass=ABCMeta):
    """
    Базовый класс универсального сборщика дагов

    :param dag_name: уникальное имя дага
    :type dag_name: str
    """
    dag_default_args = {
        'owner': 'dpyrin',
        'start_date': days_ago(2),
    }

    def __init__(self, dag_name):
        self.dag_name = dag_name

        self.__rebuild_ipc_domain_file()

    def _create_dag(self):
        dag = DAG(
            dag_id=self.dag_name or 'default_dag_name',
            default_args=self.dag_default_args,
            schedule_interval=None,
            catchup=False,
            orientation='TB'
        )

        return dag

    @staticmethod
    def __rebuild_ipc_domain_file():
        rebuild_domain_ipc()

    @abstractmethod
    def build(self):
        raise NotImplementedError(
            'Define a execute in %s.' % self.__class__.__name__
        )