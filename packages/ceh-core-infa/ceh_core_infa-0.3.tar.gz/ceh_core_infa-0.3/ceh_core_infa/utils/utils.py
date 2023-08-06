import os

from datetime import datetime
from typing import Tuple, List, Dict, Any

import psycopg2

from ..libs.models.resource_state import (
    Version,
    State,
    StateDt,
    Source,
    SourceDt,
    Origin,
    Delta,
    Target,
    Operation,
)

from ..config import SYSTEM_FOLDER, TEMPLATE_DOMAIN, IPC_TEMPLATE
from ..libs.clients.ceh_resource_client import CehResourse
from ..libs.exceptions.exception import ResourceStateException


def create_unique_folder(
        prefix: str = '',
        domain: str = None,
        path: str = SYSTEM_FOLDER,
) -> str:
    name = '/%s_%s' % (prefix, datetime.now().strftime("%Y-%m-%d-%H.%M"))

    if not os.path.exists(path):
        raise FileNotFoundError(f'No such file or directory: {path}')

    if domain:
        path = path + domain

    if not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(path + name):
        os.mkdir(path + name)

    return path + name


def generate_files_params(
        param: Dict[str, str],
        folder: str,
        wf_name: str,
        template_name: str,
        dft_fld: str = SYSTEM_FOLDER,
        domain: str = TEMPLATE_DOMAIN
) -> str:
    """Function for creating IPC configuration files based on dict"""
    filename = f'/{wf_name}-{datetime.now().timestamp()}.PARAM'
    full_path = f'{folder}{filename}'

    if os.path.exists(full_path):
        raise FileExistsError(
            f'File {filename} already exists in folder {folder}'
        )

    attr_file = [IPC_TEMPLATE, wf_name]
    for i, v in param.items():
        attr_file.append(i)
        attr_file.append(v)

    with open(f'{dft_fld}{domain}/{template_name}') as ptr:
        txt = ptr.read() % tuple(attr_file)
        with open(full_path, 'w+') as tmp:
            tmp.write(txt)

    return full_path


def create_operation(
        resource_cd: str,
        src_version_id: int,
        statement: str,
        delta: str,
        src_resource_name: int,
        tgt_table_name: str
) -> Operation:
    src_version = Version(version_id=src_version_id)
    src_state = State(version=src_version)
    src_state_dt = StateDt(max_processed_dt=datetime.now())
    source = Source(
        resource_cd=src_resource_name,
        state=src_state,
        prev_state=src_state
    )
    source_dt = SourceDt(
        resource_cd=src_resource_name,
        state=src_state_dt,
        prev_state=src_state_dt
    )
    target = Target(resource_cd=resource_cd, table=tgt_table_name)
    delta = Delta(table=delta)
    operation = Operation(
        origin=Origin(),
        delta=delta,
        statement=statement,
        sources=[source, source_dt],
        target=target
    )

    return operation


def get_conn_db(db_param: Dict[str, str]):
    return psycopg2.connect(**db_param)


def tuple2str__sql_query(iter_object: Tuple[str, ...], template: str = "'{}'"):
    assert isinstance(iter_object, tuple), 'Объект должен иметь тип tuple'

    tmp = ''

    for elem in iter_object:
        tmp = tmp + ', ' + template.format(elem) \
            if len(tmp) else tmp + template.format(elem)

    return f'({tmp})'


def get_current_records(
        iter_obj: List[Dict[str, Any]],
        key_dict: str,
        sought_elem: str
):
    cur_record = list(
        filter(
            lambda record: record[key_dict] == sought_elem, iter_obj
        )
    )

    return cur_record


def check_block(resource_cd):
    cur_res = CehResourse.get_resourse(resource_cd=resource_cd)
    if not cur_res.state:
        return False

    cur_locked = CehResourse.get_resource_state(
        resource_cd=resource_cd
    ).is_locked

    return cur_locked


def check_resource_lock(resource_cd, logger):
    logger.info(f'Checking if {resource_cd} is locked')

    resource = CehResourse.get_resourse(resource_cd=resource_cd)

    if not resource.state:
        logger.info(f'Resource {resource_cd} has no state')
        return

    is_locked = CehResourse.get_resource_state(resource_cd).is_locked

    if is_locked:
        raise ResourceStateException(f'Resource {resource_cd} is locked')

    logger.info(f'Resource {resource_cd} is not locked')
