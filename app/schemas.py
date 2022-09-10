from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional

# Schemas to define the Post structure
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime

    # * Pydantic doesn't know how to work with SQLAlchemy models, so we need to convert it to a dictionary
    class Config:
        orm_mode = True


# Schemas to define the User structure
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
