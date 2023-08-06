from typing import Union, Optional, List

from pydantic import (
    BaseModel,
    PositiveInt,
    PositiveFloat,
    Field,
    DirectoryPath,
    validator,
    AnyUrl
)


class Database(BaseModel):
    dbname: str
    host: str
    login: str
    port: int
    password: str


class BaseUrl(BaseModel):
    ceh_provider: str = Field(
        description='URL, по которому доступен провайдер ресурсов ЦЕХ',
    )
    tx_manager: str = Field(
        description='URL, по которому доступен менеджер транзакций',
    )
    ods_provider: str = Field(
        description='URL, по которому доступен провайдер ресурсов ODS',
    )
    sequence_generator: str = Field(
        description='URL, по которому доступен'
                    ' генератор последовательных чисел',
    )


class Version(BaseModel):
    ceh_provider: Union[PositiveInt, PositiveFloat]
    tx_manager: Union[PositiveInt, PositiveFloat]
    ods_provider: Union[PositiveInt, PositiveFloat]
    sequence_generator: Union[PositiveInt, PositiveFloat]


class SysSetting(BaseModel):
    load_type_cd: List[str]
    meta_version: int = None
    timeouts: int = 1000


class WorkAttempts(BaseModel):
    attempts: int = Field(
        description='Колличество доступных '
                    'попыток при ошибке в работе оператора',
    )
    timeout: int = Field(
        description='Таймаут между попытками',
    )

    @validator('attempts')
    def check_attempts(cls, v):
        if v <= 0 or v > 100:
            raise ValueError(
                'The number must not be less than 0 or greater than 100'
            )
        return v

    @validator('timeout')
    def check_timeout(cls, v):
        if v <= 0 or v > 3600:
            raise ValueError(
                'The number must not be less than 0 or greater than 3600'
            )
        return v


class Timeout(BaseModel):
    tx_timeout: int = 1000


class Services(BaseModel):
    base_url: BaseUrl
    versions: Version


class Loader(BaseModel):
    loader: str = 'only_new'

    @validator('loader')
    def check_loader(cls, v):
        if v not in {'only_new', 'all', 'wait_all'}:
            raise ValueError(
                'It can take only one of the values - only_new, all, wait_all'
            )
        return v


class Dag(BaseModel):
    work_attempts: WorkAttempts
    load_resource: Loader


class IPC(BaseModel):
    login: str
    password: str
    host: str
    port: int
    domain: str
    service: str
    template: str
    path_local_client: DirectoryPath
    path_local_conf_file: str
    wf_name_prp: str
    wf_name_load: str
    dbconnection: str


class SysFolder(BaseModel):
    path: DirectoryPath
    template: str


class Auth(BaseModel):
    auth_enable: bool = False
    oauth_client_id: Optional[str] = None
    oauth_client_secret: Optional[str] = None
    oauth_token_url: Optional[AnyUrl] = None


class Settings(BaseModel):
    gp: Database
    services: Services
    dags: Dag
    ipc: IPC
    sysfolder: SysFolder
    auth: Auth
    syssetting: SysSetting
