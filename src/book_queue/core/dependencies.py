"""
this file holds the declarations of dependencies for the fastapi app endpoints
"""

from typing import Generator

import jwt
from fastapi import Depends, HTTPException
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from starlette import status

from book_queue.core.database import DBHandler, SessionLocal, engine
from book_queue.core.schemas import TokenData
from book_queue.core.security import ALGORITHM, SECRET_KEY, oauth2_scheme
from book_queue.models.models import User
from book_queue.services.user_service import UserService

db_handler: DBHandler = DBHandler(engine, SessionLocal)


def get_db() -> Generator[Session]:
    """
    get a db session from the db_handler DBHandler class instance
    :return: yield a database session
    """
    yield from db_handler.get_session()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    user_service: UserService = UserService(db)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data: TokenData = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = user_service.get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user
