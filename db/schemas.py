from typing import List, Optional
from pydantic import BaseModel,Field,validator
from datetime import datetime

"""
title
type: ChoiceField (e.g. text or image)
created_by
created_at
updated_at
is_add_choices_active
is_voting_active
"""
class NoneDefaultModel(BaseModel):
    @validator("*", pre=True)

    def not_none(cls, v, field):
        if field.default and v is None:
            return field.default
        else:
            return v

class PollBase(NoneDefaultModel):
    title: str
    type: str
    is_add_choices_active: bool
    is_voting_active: bool
    # created_by: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class PollCreate(PollBase):
    pass

class Poll(PollBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

"""
username
email
created_at
updated_at
"""
class UserBase(NoneDefaultModel):
    username: str
    email: str
    created_at: Optional[datetime]#Field(default_factory=datetime.now)
    updated_at: Optional[datetime]#Field(default_factory=datetime.now)

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    polls: List[Poll] = []

    class Config:
        orm_mode = True
