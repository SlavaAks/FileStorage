
from fastapi import FastAPI,status,Depends,HTTPException
from pydantic import BaseModel,EmailStr

from auth import Auth
from database import engine
from schemas import User, UserCreate, UserLogIn

from repository.user_rep import UserRepository
from models import Model

Model.metadata.create_all(bind=engine)
app = FastAPI()





@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/signup/",response_model=User,status_code=status.HTTP_201_CREATED)
async def registration(user:UserCreate,users:UserRepository=Depends()):
    db_user=users.find_by_username(user.username)
    print(user.password)
    if db_user:
        raise HTTPException( status_code=400,
            detail="User with the same username already exist")

    db_user=users.create(user)
    return User.from_orm(db_user)


@app.post('/login')
async def login(user:UserLogIn,users:UserRepository=Depends(),auth:Auth=Depends()):
    db_user=users.find_by_username(user.username)

    if not db_user:
        return HTTPException(status=status.HTTP_401_UNAUTHORIZED,detail="Invalid username")

    if not auth.verify_password(user.password,db_user.hashed_password):
        return HTTPException(status=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    access_token = auth.encode_token(user.username)
    refresh_token=auth.encode_refresh_token(user.username)

    return {'access_token':access_token,'refresh_token':refresh_token}


