from pydantic import BaseModel
from typing import List


class Role(BaseModel):
    id: int
    name: str
    users: List[int]


class User(BaseModel):
    username: str
    id: int
    roles: List[int] = []
