from ....libs.ipc.parameters.parameters import LaunchParam
from ..operators.operators import IPCLaunchOperator
from ..operators.create_tx_operator import CreateTransactionOperator
from ..operators.update_resource_state_operator import UpdateResourceStateOperator
from ..operators.commit_transaction_operator import CommitTransactionOperator
from ..operators.rollback_transaction_operator import RollbackTransactionOperator
from ..operators.check_resource_locking_operator import CheckResourceLockingOperator
from ..operators.locked_resources_operator import LockedGroupResourcesOperator
from ....config import ATTEMPS_DAG_CONF, TIMEOUT_DAG_CONF


def generate_ipc_task(
        dag,
        tsk_id,
        raw_params: str,
        slv_wf_name: str,
        workflow: str,
        prefix: str = None,
        attempts: int = ATTEMPS_DAG_CONF,
        timeout: int = TIMEOUT_DAG_CONF
) -> IPCLaunchOperator:
    """
    Собирает все данные необходимые для зпуска потока
    и возвращает класс оператор для ipc
    """
    params = LaunchParam(
        raw_params=raw_params,
        is_depth_search=True,
        not_case_dependency=True,
        wait=workflow,
        prefix=prefix
    )

    task = IPCLaunchOperator(
        task_id=f'{tsk_id}_{slv_wf_name}',
        ipc_params=params.get_prarams(),
        dag=dag,
        debug_mode=True,
        attempts=attempts,
        timeout=timeout
    )

    return task


def generate_open_tx_task(dag, global_params) -> CreateTransactionOperator:
    """
    Генерирует таск для создания общей транзакции
    :param dag: текущий объект дага
    :param global_params: текущий обеъект потока из xcom
    :return: таск
    """
    open_tx = CreateTransactionOperator(
        task_id=f'open_transactions',
        xcom_params=global_params,
        dag=dag,
        task_concurrency=1
    )

    return open_tx


def generate_task_update_state(
        dag,
        global_params,
        slv_wf_name,
        attempts: int = ATTEMPS_DAG_CONF,
        timeout: int = TIMEOUT_DAG_CONF
) -> UpdateResourceStateOperator:
    """
    Генерируем таск для обновления состояния
    :param dag: текущий объект дага
    :param global_params: текущий обеъект потока из xcom
    :param slv_wf_name: имя источника
    :param attempts: колличество попыток в случае ошибки
    :param timeout: таймаут между попытками
    :return:
    """
    task = UpdateResourceStateOperator(
        task_id=f'update_state_resources_{slv_wf_name}',
        slw_wf_name=slv_wf_name,
        global_params=global_params,
        dag=dag,
        attempts=attempts,
        timeout=timeout,
        task_concurrency=1
    )

    return task


def generate_commit_tx_task(
        dag,
        tx_info,
        resources,
        attempts: int = ATTEMPS_DAG_CONF,
        timeout: int = TIMEOUT_DAG_CONF
) -> CommitTransactionOperator:
    """
    Генерируем таск коммита транзакции
    :param dag: текущий объект дага
    :param tx_info: Словарь с информацией о транзакции
    :param resources: Список необходимых ресурсов
    :param attempts: колличество попыток в случае ошибки
    :param timeout: таймаут между попытками
    :return: таск
    """
    commit_trx = CommitTransactionOperator(
        task_id='commit',
        tx_info=tx_info,
        resources=resources,
        error_if_locked=True,
        attempts=attempts,
        timeout=timeout,
        dag=dag,
        trigger_rule='all_success'
    )

    return commit_trx


def generate_rollback_tx_task(
        dag,
        tx_info,
        resources,
        attempts: int = ATTEMPS_DAG_CONF,
        timeout: int = TIMEOUT_DAG_CONF

) -> RollbackTransactionOperator:
    """
    Генерируем таск ролбека транзакции
    :param dag: текущий объект дага
    :param tx_info: словарь с информацией о транзакции
    :param resources: список необходимых ресурсов
    :param attempts: колличество попыток в случае ошибки
    :param timeout: таймаут между попытками
    :return: таск
    """
    rollback_trx = RollbackTransactionOperator(
        task_id=f'rollback',
        tx_info=tx_info,
        resources=resources,
        error_if_locked=False,
        attempts=attempts,
        timeout=timeout,
        dag=dag,
        trigger_rule='one_failed'
    )

    return rollback_trx


def generate_check_block_resources_task(
        dag,
        slv_wf_name,
        resources,
        attempts=ATTEMPS_DAG_CONF,
        timeout=TIMEOUT_DAG_CONF
) -> CheckResourceLockingOperator:
    """
    Генерируем таск блокировки ресурса
    :param dag: текущий объект дага
    :param slv_wf_name: текущий источник
    :param resources: необходимые ресурсы
    :param attempts: колличество попыток в случае ошибки
    :param timeout: таймаут между попытками
    :return:
    """
    check_block = CheckResourceLockingOperator(
        task_id=f'check_blocking_resources_{slv_wf_name}',
        resources=resources,
        attempts=attempts,
        timeout=timeout,
        dag=dag,
    )

    return check_block


def generate_locked_resources_task(
        dag,
        slv_wf_name,
        resources,
        tx_info,
        attempts=ATTEMPS_DAG_CONF,
        timeout=TIMEOUT_DAG_CONF
) -> LockedGroupResourcesOperator:
    """
    Генерируем таск для блокировки ресурсов
    :param dag: текущий объект дага
    :param slv_wf_name: текущий источник
    :param resources: необходимые ресурсы
    :param tx_info: словарь с информацией о транзакции
    :param attempts: колличество попыток в случае ошибки
    :param timeout: таймаут между попытками
    :return:
    """
    task = LockedGroupResourcesOperator(
        task_id=f'blocking_all_resources_{slv_wf_name}',
        resources=resources,
        tx_info=tx_info,
        attempts=attempts,
        timeout=timeout,
        dag=dag,
    )

    return task
