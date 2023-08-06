from typing import Optional, Union
from datetime import datetime
from pydantic import BaseModel


class TxUid(BaseModel):
    tx_uid: Optional[str]


class TxToken(BaseModel):
    tx_token: str = None


class TxUrl(TxToken):
    url: str


class TxStatus(BaseModel):
    start_dttm: Optional[datetime]
    finish_dttm: Optional[datetime]
    is_active: Optional[bool]
    is_committed: Optional[bool]
    is_readonly: bool = None
    consented_to_commit: bool = None
    client_committed: Optional[bool]


class TxStage(BaseModel):
    stage_no: int
    start_dttm: Optional[datetime]
    finish_dttm: Optional[datetime]


class TxCommitTimeout(BaseModel):
    commit_timeout: Optional[Union[str, int]]


class TxChangeCommitTimeout(TxToken, TxCommitTimeout):
    pass


class TxBase(TxUid, TxToken, TxCommitTimeout):
    status: TxStatus
    stage: TxStage


class Transaction(TxBase):
    def __eq__(self, other):
        return other == self.resource_cd
