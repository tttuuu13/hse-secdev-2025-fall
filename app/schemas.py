from datetime import datetime
from typing import List

from pydantic import BaseModel


class LabelBase(BaseModel):
    name: str


class LabelCreate(LabelBase):
    pass


class Label(LabelBase):
    id: int

    model_config = {"from_attributes": True}


class IssueBase(BaseModel):
    title: str
    status: str = "open"


class IssueCreate(IssueBase):
    pass


class Issue(IssueBase):
    id: int
    owner_id: int
    created_at: datetime
    labels: List[Label] = []

    model_config = {"from_attributes": True}


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    issues: List[Issue] = []

    model_config = {"from_attributes": True}
