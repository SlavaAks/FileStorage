from functools import lru_cache
from sqlalchemy.orm import Session
import config
import database
from auth import Auth
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
# Вызывается по время внедрения зависимости
def get_db() -> Session:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Возврат существующего экземпляра DBSettings вместо создания нового
@lru_cache
def get_db_settings() -> config.DBSettings:
    return config.DBSettings()





oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


async def get_current_user(token: str = Depends(oauth2_scheme),auth:Auth=Depends()):
    username = auth.decode_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username