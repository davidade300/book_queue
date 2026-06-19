from fastapi import APIRouter, Depends
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


