from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from book_queue.core.dependencies import get_db
from book_queue.core.schemas import CreateUserRequest
from book_queue.services.user_service import UserService

router = APIRouter()


@router.post('/auth/', status_code=status.HTTP_201_CREATED)
async def create_user(
    user_request: CreateUserRequest, db: Session = Depends(get_db)
):
    user_service: UserService = UserService(db)
    user_service.create_user(user_request)

@router.post('/token/', status_code=status.HTTP_201_CREATED)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user_service: UserService = UserService(db)
    user = user_service.authenticate_user(form_data.username, form_data.password)
