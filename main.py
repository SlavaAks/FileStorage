from typing import List

from fastapi import FastAPI, status, Depends, HTTPException




from auth_bearer import JWTBearer, Auth
from database import engine
from schemas import User, UserCreate, UserLogIn, FileBase

from repository.user_rep import UserRepository
from models import Model
from router import file_route,auth_route

Model.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(file_route.router)
app.include_router(auth_route.router)


@app.get("/")
async def root():
    return {"message": "File Storage"}





