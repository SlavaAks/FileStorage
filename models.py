from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Model


class User(Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username=Column(String,unique=True,index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

