from fastapi import FastAPI
from pydantic import BaseModel,EmailStr

app = FastAPI()

class User:
    first_name:str
    second_name:str
    login:str
    email:EmailStr



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/signup/")
async def registration():
    pass