from typing import List
from uuid import UUID

from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

from models import User
from dependencies import get_db
from schemas import UserCreate
from passlib.context import CryptContext

class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db  # произойдет внедрение зависимостей

    def find(self, id: int) -> User:
        query = self.db.query(User)
        return query.filter(User.id == id).first()

    def find_by_username(self, username: str):
        query = self.db.query(User)
        return query.filter(User.username == username).first()

    def all(self, skip: int = 0, max: int = 100) -> List[User]:
        query = self.db.query(User)
        return query.offset(skip).limit(max).all()

    def create(self, user: UserCreate) -> User:
        hasher = CryptContext(schemes=['bcrypt'])
        pass_hash = hasher.hash(user.password)

        db_user = User(    #**user.dict()
            username=user.username,
            email=user.email,
            hashed_password=pass_hash
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user