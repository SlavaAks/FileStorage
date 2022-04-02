from typing import List, Optional

from pydantic import BaseModel,EmailStr


class UserBase(BaseModel):
    username:str

class UserLogIn(UserBase):
    password:str

class UserCreate(UserBase):
    password: str
    email: EmailStr

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True