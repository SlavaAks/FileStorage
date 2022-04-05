from typing import List, Optional

from pydantic import BaseModel,EmailStr,validator


class UserBase(BaseModel):
    username:str

class UserLogIn(UserBase):
    password:str

class UserCreate(UserBase):
    password: str
    email: EmailStr

class User(UserBase):
    id: int
    email:EmailStr
    is_active: bool

    class Config:
        orm_mode = True

class FileBase(BaseModel):
    filename:str

    class Config:
        orm_mode = True