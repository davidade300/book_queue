
from sqlalchemy.orm import Session

from book_queue.core.schemas import (
    BookResponse,
    BookResponseList,
    CreateBookRequest,
)
from book_queue.models.models import Book
from book_queue.services.book_service import BookService


def test_create_book(test_client, book_request: CreateBookRequest):
    response = test_client.post(
        '/books', json=book_request.model_dump(mode='json')
    )
    json_book: BookResponse = BookResponse.model_validate(response.json())

    assert response.status_code == 201
    assert json_book.title == 'Test'
    assert json_book.author == 'Test Author'
    assert json_book.id == 1


def test_get_book_by_id(
    test_client, db_session: Session, book_request: CreateBookRequest
):
    book: Book = BookService(db_session).create(book_request)

    response = test_client.get(f'/books/get/{book.id}')
    json_book: BookResponse = BookResponse.model_validate(response.json())

    assert response.status_code == 200
    assert json_book.id == book.id
    assert json_book == BookResponse.model_validate(book)


def test_list_books(
    test_client, db_session: Session, book_request: CreateBookRequest
):
    book: Book = BookService(db_session).create(book_request)

    response = test_client.get('/books/list')
    json_books: BookResponseList = BookResponseList.model_validate(
        response.json()
    )

    assert response.status_code == 200
    assert len(json_books.books) == 1
    assert json_books.books[0] == BookResponse.model_validate(book)
