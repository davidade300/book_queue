from fastapi import APIRouter
from sqlalchemy.orm import Session
from starlette import status

from book_queue.core.dependencies import db_dependecy
from book_queue.core.schemas import BookResponse, CreateBookRequest
from book_queue.models.models import Book
from book_queue.services.book_service import BookService

router = APIRouter(prefix='/books', tags=['books'])


@router.post(
    '/', response_model=BookResponse, status_code=status.HTTP_201_CREATED
)
def create_book(
    request: CreateBookRequest, db: Session = db_dependecy
) -> BookResponse:
    book_service: BookService = BookService(db)
    book: Book = book_service.create(request)

    return BookResponse.model_validate(book)


@router.get('/get/{book_id}', response_model=BookResponse, status_code=status.HTTP_200_OK)
def get_book_by_id(book_id: int, db: Session = db_dependecy) -> BookResponse:
    book_service: BookService = BookService(db)
    book = book_service.get_by_id(book_id)

    return BookResponse.model_validate(book)
