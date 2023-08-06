import os

import yaml

from typing import List, Dict, Union, Tuple
from .libs.models.settings import Settings

__PATH_CORE_CONFIG: str = os.getenv(
    key='CORE_FILE_CONFIG',
    default='/mnt/c/pythonProject/ceh_core_infa/core_config.yml'
)


def get_object_params(path2config):
    """Loading and validating the config"""
    with open(path2config, 'r') as stream:
        yaml2json = yaml.safe_load(stream)

        conf = Settings(**yaml2json)

    return conf


config: Settings = get_object_params(
    __PATH_CORE_CONFIG
)  # Загуржаем и валидируем конфиг

# Глобальные системные настройки
LOAD_TYPE_CD: List[str] = config.syssetting.load_type_cd
META_VERSION: str = os.getenv(
    key='META_VERSION',
    default=config.syssetting.meta_version
)

# Версия API
BASE_URL_CEH_PROVIDER: str = config.services.base_url.ceh_provider
VERSION_CEH_PROVIDER: float = config.services.versions.ceh_provider

# Версия API
BASE_URL_SEQ_GENERATOR: str = config.services.base_url.sequence_generator
VERSION_CEH_SEQ_GENERATOR: float = config.services.versions.sequence_generator

# Версия API
BASE_URL_TX_MANAGER: str = config.services.base_url.tx_manager
VERSION_TX_MANAGER: float = config.services.versions.tx_manager

# Глобальный параметр кол-ва поток и жвремени ожидая между ними
ATTEMPS_DAG_CONF: int = config.dags.work_attempts.attempts
TIMEOUT_DAG_CONF: int = config.dags.work_attempts.timeout

# Парметры загрузки версий
PARAMS_LOADING: str = config.dags.load_resource.loader

# Путь к системный папки для хранения системной информации
SYSTEM_FOLDER: str = str(config.sysfolder.path)
# Домен к папке с шаблонами
TEMPLATE_DOMAIN: str = '/Template'

# Величина таймаута транзакции
TX_TIMEOUT = config.syssetting.timeouts

# Настройки для БД
DB_QUERY_RESOURCES: str = '''SELECT
    main_wf_name,
    slv_wf_name,
    tgt_resource_name,
    src_resource_name,
    tgt_table_name
FROM etl.v_wf_workflow_res_ref
WHERE
    load_type_cd='%s' AND
    meta_version_id='%s' AND
    main_wf_name IN %s
'''

DB_QUERY__DELTA_STATEMENT = '''SELECT
    o_dlt_name, o_sql_text
FROM etl.f_get_upload_expr(%s, '%s', %s)
'''

# Параметры Greenplum
DB_PARAMS: Dict[str, str] = {
    'host': config.gp.host,
    'port': config.gp.port,
    'dbname': config.gp.dbname,
    'user': config.gp.login,
    'password': config.gp.password
}

# Настройки для IPC
IPC_MAIN_FOLDER = config.ipc.path_local_client
IPC_CLIENT_FOLDER: str = f'{IPC_MAIN_FOLDER}/PowerCenter/server/bin/pmcmd'

# Логин/Пароль IPC, строго определен в файле конфигурации
IPC_LOGIN: str = config.ipc.login
IPC_PASSWORD: str = config.ipc.password

# Хост/Порт IPC
IPC_HOST: str = config.ipc.host
IPC_PORT: int = config.ipc.port

# Авторизация
AUTH_ENABLE = config.auth.auth_enable
OAUTH_CLIENT_ID = config.auth.oauth_client_id
OAUTH_CLIENT_SECRET = config.auth.oauth_client_secret
OAUTH_TOKEN_URL = config.auth.oauth_token_url

# Имя конекшна IPC к целевой БД
DB_CONNECTION: str = config.ipc.dbconnection

# ППР
WF_NAME_PRP: str = config.ipc.wf_name_prp

# ПЗД
WF_NAME_LOAD: str = config.ipc.wf_name_load

ALL_WF: Tuple = (WF_NAME_PRP, WF_NAME_LOAD)

# Домен папки с конфигурационными файлами IPC
PATH_CONFIG_FILES_IPC: str = config.ipc.path_local_conf_file or '/Workflow'
# Стандартный темплейт, по умолчанию из конфигурационного файла
IPC_TEMPLATE: str = config.ipc.template or 'TEST_TEMPLATE'

IPC_DOMAIN: str = config.ipc.domain
IPC_SERVICE: str = config.ipc.service

# Шаблон для запуска потоков IPC
DEFAULT_PARAMS_FOR_PREPARE: Dict[str, Union[str, int, None]] = {
    'DBConnection_ODBC': None,
    'INSTANCE_ID': None,
    'SRC_VERSION_ID': None,
    'META_VERSION_ID': None,
    'PREV_DATA_LOAD_DT': None,
    'WORKFLOW_NAME': None,
    'AUTOINC_SRV_URL': None,
}

DEFAULT_PARAMS_FOR_LOAD: Dict[str, Union[str, int, None]] = {
    'DBConnection_ODBC': None,
    'INSTANCE_ID': None,
    'TGT_CUR_VERSION_ID': None,
    'META_VERSION_ID': None,
    'WORKFLOW_NAME': None,
    'AUTOINC_SRV_URL': None,
}

IPC_DEFAULT_ARGS = {
    'user': IPC_LOGIN,
    'password': IPC_LOGIN,
    'folder': IPC_TEMPLATE,
    'domain': IPC_DOMAIN,
    'service': IPC_SERVICE
}

INFA_HOME: str = f'{IPC_MAIN_FOLDER}/PowerCenter'
LD_LIBRARY_PATH: str = f'{""}:{IPC_MAIN_FOLDER}/PowerCenter/server/bin'
PATH: str = f'/usr/local/sbin:/usr/local/bin:' \
            f'/usr/sbin:/usr/bin:/sbin:/bin:{IPC_MAIN_FOLDER}/PowerCenter'
INFA_DOMAINS_FILE: str = f'{IPC_MAIN_FOLDER}/domains.infa'

# Переменные окружения для запуска потоков IPC через pmcmd
ENVIRONMENT: Dict[str, str] = {
    'INFA_HOME': INFA_HOME,
    'LD_LIBRARY_PATH': LD_LIBRARY_PATH,
    'PATH': PATH,
    'INFA_DOMAINS_FILE': INFA_DOMAINS_FILE
}

DEV_IPC_CONF = {
    'service': 'IPC_IAS',
    'domain': 'VTB_DOM',
    'folder': 'TEST_TEMPLATE',
    'instance': 'WF_TEMPLATE1',
    'wait': 'WF_TEMPLATE1',
}
