from pydantic import BaseModel


class Increment(BaseModel):
    key: str
    value: int


class CreateIncrement(BaseModel):
    increment: int
