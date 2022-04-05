from typing import List
from uuid import UUID

from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

from models import File

from dependencies import get_db
from passlib.context import CryptContext

class FileRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db  # произойдет внедрение зависимостей

    def find(self, id: int) -> File:
        query = self.db.query(File)
        return query.filter(File.id == id).first()

    def url_exist(self,url:str):
        query = self.db.query(File)
        return query.filter(File.url == url).first()

    def find_user_file(self, username: str):
        query = self.db.query(File)
        return query.filter(File.owner_username == username).all()


    def create(self, url,owner_username,filename) -> File:
        db_file = File(    #**user.dict()
            url=url,
            owner_username=owner_username,
            filename=filename,
        )

        self.db.add(db_file)
        self.db.commit()
        self.db.refresh(db_file)

        return db_file