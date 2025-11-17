from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class LabelBase(BaseModel):
    name: str


class LabelCreate(LabelBase):
    pass


class Label(LabelBase):
    id: int

    model_config = {"from_attributes": True}


class IssueBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    status: str = "open"


class IssueCreate(IssueBase):
    pass


class IssueUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    status: str | None = None


class Issue(IssueBase):
    id: int
    owner_id: int
    created_at: datetime
    labels: List[Label] = []

    model_config = {"from_attributes": True}


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class User(UserBase):
    id: int
    role: str
    issues: List[Issue] = []

    model_config = {"from_attributes": True}
