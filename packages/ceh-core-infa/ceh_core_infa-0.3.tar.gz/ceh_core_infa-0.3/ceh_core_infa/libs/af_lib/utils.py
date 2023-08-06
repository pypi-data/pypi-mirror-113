from sqlalchemy.sql import desc

from airflow.models import Pool, XCom
from airflow.utils.db import provide_session


@provide_session
def create_new_poll(pool_name: str, slots: int, session=None) -> None:
    pool = (
        session.query(Pool).filter(
            Pool.pool == pool_name
        ).first())

    if not pool:
        session.add(Pool(pool=pool_name, slots=slots))
        session.commit()


@provide_session
def get_xcom_ipcparam(dag_id, key, session=None) -> XCom:
    """Get param for ipc launch from xcom"""
    result = session.query(
        XCom
    ).filter(
        XCom.dag_id == dag_id
    ).filter(
        XCom.key == key
    ).order_by(
        desc(XCom.execution_date)
    ).limit(1).scalar()

    return result


def update_xcom_ipcparam(
        key: str,
        value: str,
        task_id: str,
        dag_id: str,
        execution_date
):
    XCom.set(
        key=key,
        value=value,
        task_id=task_id,
        dag_id=dag_id,
        execution_date=execution_date
    )


def parse_xcom_ipcparam(params, wf_id):
    tgt_resource_cd = params[wf_id]['tgt_resource_name']
    tgt_table_name = params[wf_id]['tgt_table_name']
    src_resource_name = params[wf_id]['src_resource_name']
    wf_name = params[wf_id]['slv_wf_name']
    instance_id = params[wf_id]['prepare_param']['INSTANCE_ID']
    tx_uid = params[wf_id]['tx_info']['tx_uid']
    tx_token = params[wf_id]['tx_info']['tx_token']
    return (
        tgt_resource_cd,
        tgt_table_name,
        src_resource_name,
        instance_id,
        wf_name,
        tx_uid,
        tx_token
    )
