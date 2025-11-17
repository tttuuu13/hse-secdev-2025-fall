from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr, Field


class LabelBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)


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
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class User(UserBase):
    id: int
    role: str
    issues: List[Issue] = []

    model_config = {"from_attributes": True}
