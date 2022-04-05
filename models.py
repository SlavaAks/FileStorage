from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Model
from datetime import datetime

class User(Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username=Column(String,unique=True,index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("File", back_populates="owner")

class File(Model):
    __tablename__="files"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String,unique=True,index=True)
    owner_username = Column(String, ForeignKey("users.username"))
    filename = Column(String)
    create_date = Column(DateTime, default=datetime.now)

    owner = relationship("User", back_populates="items")
