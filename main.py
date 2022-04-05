from typing import List

from fastapi import FastAPI, status, Depends, HTTPException, UploadFile, File,Body,Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

from repository.file_rep import FileRepository
from auth_bearer import JWTBearer, Auth
from database import engine
from schemas import User, UserCreate, UserLogIn, FileBase

from repository.user_rep import UserRepository
from models import Model
from dependencies import get_current_user
import shutil
import os



Model.metadata.create_all(bind=engine)
app = FastAPI()







@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str,user:str=Depends(get_current_user)):
    return {"message": f"Hello {name+user}"}


@app.post("/signup/", response_model=User, status_code=status.HTTP_201_CREATED)
async def registration(user: UserCreate, users: UserRepository = Depends()):
    db_user = users.find_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400,
                            detail="User with the same username already exist")

    db_user= users.find_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400,
                            detail="User with the same email already exist")
    db_user = users.create(user)
    return User.from_orm(db_user)


@app.post('/login/')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), users: UserRepository = Depends(), auth: Auth = Depends()):
    db_user = users.find_by_username(form_data.username)

    if not db_user:
        raise HTTPException(status=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid username",
                            headers={"WWW-Authenticate": "Bearer"},)

    if not auth.verify_password(form_data.password, db_user.hashed_password):

        raise HTTPException(status=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid password",
                            headers={"WWW-Authenticate": "Bearer"},)

    access_token = auth.encode_token(form_data.username)
    refresh_token = auth.encode_refresh_token(form_data.username)

    return {'access_token': access_token, 'refresh_token': refresh_token}



@app.post('/file_uploader/')
async def file_upload(file: bytes = File(...,max_length=15000000),
                      file_name:str=Body(...),user:str=Depends(get_current_user),
                      repfile:FileRepository=Depends()):


    if not os.path.exists(f"./media/{user}"):
        os.mkdir(f"./media/{user}")
    with open(f'./media/{user}/{file_name}','wb') as buffer:
        buffer.write(file)
    url=repfile.url_exist(f'./media/{user}/{file_name}')
    print(url)
    if url:
        raise HTTPException(status_code=400,
                            detail="file with the same name already exist")
    repfile.create(f'./media/{user}/{file_name}',user,file_name)

    return {'filename':file_name,'size':len(file)}


@app.get("/files/{username}/",response_model=List[FileBase])
async def file_list(username:str,user:str=Depends(get_current_user),repfile:FileRepository=Depends()):
    if username != user:
       raise HTTPException(status_code=405,
                           detail="no access",)
    files=repfile.find_user_file(username)
    return files

@app.delete("/files/{username}/{filename}")
async def file_list(username:str,user:str=Depends(get_current_user),repfile:FileRepository=Depends()):
    if username != user:
       raise HTTPException(status_code=405,
                           detail="no access",)
    files=repfile.find_user_file(username)
    return files
