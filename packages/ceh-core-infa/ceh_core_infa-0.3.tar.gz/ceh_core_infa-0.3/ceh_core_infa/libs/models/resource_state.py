import datetime

from typing import Union, List, Optional

from pydantic import BaseModel


class Version(BaseModel):
    version_id: int


class State(BaseModel):
    version: Version


class StateDt(BaseModel):
    max_processed_dt: datetime.datetime


class Source(BaseModel):
    resource_cd: str
    state: State
    prev_state: State


class SourceDt(Source):
    state: StateDt
    prev_state: StateDt


class Delta(BaseModel):
    table: str


class Target(BaseModel):
    resource_cd: str
    table: str


class Status(BaseModel):
    start_dttm: datetime.datetime
    finish_dttm: Optional[datetime.datetime] = None
    is_active: bool
    is_committed: bool


class Origin(BaseModel):
    additionalProp1: str = 'string'
    additionalProp2: str = 'string'
    additionalProp3: str = 'string'


class Operation(BaseModel):
    origin: Origin
    sources: List[Union[Source, SourceDt]]
    statement: str
    delta: Delta
    target: Target
    status: Optional[Status]


class ResourceStateUpdate(BaseModel):
    tx_uid: str
    operation: Operation = None


class ResourceVersion(BaseModel):
    version_id: int
    tx_uid: str
    operations: List[Operation] = None
    status: Status


class ResourceState(BaseModel):
    resource_cd: str
    is_locked: bool
    locked_by: int
    as_of_dttm: datetime.datetime
    version: ResourceVersion
