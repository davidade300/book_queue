from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from book_queue.core import schemas
from book_queue.core.dependencies import get_current_active_user, get_db
from book_queue.core.schemas import CreateUserRequest, Token
from book_queue.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
)
from book_queue.models.models import User
from book_queue.services.auth_service import AuthService
from book_queue.services.user_service import UserService

router = APIRouter()


@router.post('/auth/', status_code=status.HTTP_201_CREATED)
async def create_user(
    user_request: CreateUserRequest, db: Session = Depends(get_db)
):
    user_service: UserService = UserService(db)
    user_service.create_user(user_request)


@router.post('/token')
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    user = AuthService(db).authenticate_user(
        form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    acess_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=acess_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')


@router.get('/auth/me/')
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
) :
    return current_user


