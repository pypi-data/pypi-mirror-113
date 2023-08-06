import warnings

from datetime import timedelta
from typing import List

from airflow.models import DAG

from airflow.operators.subdag_operator import SubDagOperator
from airflow.operators.dummy_operator import DummyOperator

from ...libs.ipc.parameters.parameters import LaunchParam
from .operators.operators import IPCLaunchOperator
from .operators.create_tx_operator import CreateTransactionOperatorOld
from .operators.update_resource_state_operator import UpdateResourceStateOperatorOld
from .operators.commit_transaction_operator import CommitTransactionOperatorOld
from .operators.rollback_transaction_operator import RollbackTransactionOperatorOld
from .operators.check_resource_locking_operator import CheckResourceLockingOperatorOld
from .operators.locked_resources_operator import LockedGroupResourcesOperatorOld

from ...config import ATTEMPS_DAG_CONF, TIMEOUT_DAG_CONF

from .utils import create_new_poll, get_xcom_ipcparam

warnings.simplefilter('always', DeprecationWarning)
warnings.warn(
            'Работа через dynamic_dag в следующих релизах поддерживаться не будет',
            DeprecationWarning,
        )


def generate_sub_dag_ipc(
        dag,
        sd_id,
        caller_dag_id,
        pool_name,
        key_x,
        prefix,
        workflow,
        attempts=ATTEMPS_DAG_CONF,
        timeout=TIMEOUT_DAG_CONF
) -> SubDagOperator:
    """Create subdag object with IPCOperator"""

    create_new_poll(pool_name=pool_name, slots=64)

    sub_dag = DAG(
        dag_id=f'{dag.dag_id}.{sd_id}',
        params=dag.params,
        default_args=dag.default_args,
        template_searchpath=dag.template_searchpath,
        user_defined_macros=dag.user_defined_macros,
    )

    gp = get_xcom_ipcparam(
        dag_id=caller_dag_id,
        key=key_x
    )

    tasks = []

    start = DummyOperator(task_id='start_task', dag=sub_dag, pool=pool_name)

    if gp:
        for key, value in gp.value.items():
            a = LaunchParam(
                raw_params=value,
                is_depth_search=True,
                not_case_dependency=True,
                wait=workflow,
                prefix=prefix
            )

            task = IPCLaunchOperator(
                task_id='{}-{}'.format(key, value['slv_wf_name']),
                ipc_params=a.get_prarams(),
                dag=sub_dag,
                debug_mode=True,
                pool=pool_name
            )

            tasks.append(task)

        start.set_downstream(tasks)

    sd_task = SubDagOperator(
        task_id=sd_id,
        subdag=sub_dag,
        retries=attempts,
        retry_delay=timedelta(seconds=timeout),
        dag=dag,
        depends_on_past=False,
        trigger_rule='all_success',
    )

    return sd_task


def open_general_tx_old(dag, key_x, caller_dag_id) -> CreateTransactionOperatorOld:
    gp = get_xcom_ipcparam(
        dag_id=caller_dag_id,
        key=key_x
    )

    open_tx = CreateTransactionOperatorOld(
        task_id='open_transactions',
        xcom_params=gp,
        dag=dag
    )

    return open_tx


def generate_group_tasks_tx(
        dag,
        key_x,
        caller_dag_id
) -> List[CreateTransactionOperatorOld]:
    gp = get_xcom_ipcparam(
        dag_id=caller_dag_id,
        key=key_x
    )

    tasks = []

    if gp:
        for key, value in gp.value.items():
            task = CreateTransactionOperatorOld(
                task_id='{}open_tx_{}'.format(key, value['slv_wf_name']),
                xcom_params=gp,
                wf_id=key,
                dag=dag
            )
            tasks.append(task)

    return tasks


def generate_group_tasks_update_state(dag, key_x, caller_dag_id) -> List[UpdateResourceStateOperatorOld]:
    gp = get_xcom_ipcparam(
        dag_id=caller_dag_id,
        key=key_x
    )

    tasks = []

    if gp:
        for key, value in gp.value.items():
            task = UpdateResourceStateOperatorOld(
                task_id='lock_resource_{}_{}'.format(key, value['slv_wf_name']),
                wf_id=key,
                xcom_data=gp,
                dag=dag
            )
            tasks.append(task)

    return tasks


def commit_tx_old(
        dag,
        key_x,
        caller_dag_id
) -> CommitTransactionOperatorOld:
    gp = get_xcom_ipcparam(
        dag_id=caller_dag_id,
        key=key_x
    )

    commit_trx = CommitTransactionOperatorOld(
        task_id='commit',
        xcom_params=gp,
        error_if_locked=True,
        attempts=5,
        timeout=60,
        dag=dag,
        trigger_rule='all_success'
    )

    return commit_trx


def rollback_tx_old(
        dag,
        key_x,
        caller_dag_id,
        task_desc=''
) -> RollbackTransactionOperatorOld:
    gp = get_xcom_ipcparam(
        dag_id=caller_dag_id,
        key=key_x
    )

    rollback_trx = RollbackTransactionOperatorOld(
        task_id=f'rollback{task_desc}',
        xcom_params=gp,
        error_if_locked=False,
        attempts=5,
        timeout=60,
        dag=dag,
        trigger_rule='one_failed'
    )

    return rollback_trx


def check_blocking_target_resources_old(
        dag,
        key_x,
        caller_dag_id
) -> CheckResourceLockingOperatorOld:
    gp = get_xcom_ipcparam(
        dag_id=caller_dag_id,
        key=key_x
    )

    check_block = CheckResourceLockingOperatorOld(
        task_id='check_blocking_target_resources',
        xcom_params=gp,
        attempts=5,
        timeout=10,
        dag=dag,
    )

    return check_block


def locked_all_resources_old(
        dag,
        key_x,
        caller_dag_id
):
    gp = get_xcom_ipcparam(
        dag_id=caller_dag_id,
        key=key_x
    )

    locked_res = LockedGroupResourcesOperatorOld(
        task_id='blocking_all_target_resources',
        xcom_params=gp,
        attempts=5,
        timeout=10,
        dag=dag,
    )

    return locked_res



