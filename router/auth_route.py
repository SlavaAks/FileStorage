from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from auth import Auth
from repository.user_rep import UserRepository
from schemas import UserCreate, User
from dependencies import oauth2_scheme
router=APIRouter()

@router.post("/signup/", response_model=User, status_code=status.HTTP_201_CREATED)
async def registration(user: UserCreate, users: UserRepository = Depends()):
    db_user = users.find_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400,
                            detail="User with the same username already exist")

    db_user = users.find_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400,
                            detail="User with the same email already exist")
    db_user = users.create(user)
    return User.from_orm(db_user)


@router.post('/login/')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), users: UserRepository = Depends(),
                auth: Auth = Depends()):
    db_user = users.find_by_username(form_data.username)

    if not db_user:
        raise HTTPException(status=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid username",
                            headers={"WWW-Authenticate": "Bearer"}, )

    if not auth.verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid password",
                            headers={"WWW-Authenticate": "Bearer"}, )

    access_token = auth.encode_token(form_data.username)
    refresh_token = auth.encode_refresh_token(form_data.username)

    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.get('/refresh')
def refresh_token(refresh_token: str = Depends(oauth2_scheme),auth:Auth=Depends()):
    new_token =auth.refresh_token(refresh_token)
    return {'access_token':new_token}