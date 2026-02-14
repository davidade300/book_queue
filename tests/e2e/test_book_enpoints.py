from datetime import datetime

from book_queue.core.database import get_db
from book_queue.core.schemas import BookResponse, CreateBookRequest
from book_queue.models.models import Book
from book_queue.services.book_service import BookService


def test_create_book(test_client):
    new_book: CreateBookRequest = CreateBookRequest(
        title='Test',
        author='Test Author',
        edition=1,
        release_date=datetime(2020, 1, 1),
        publisher='Test Publisher',
        cover_img_url='http://cover.jpg',
        isbn_10='0123456789',
        isbn_13='0123456789123',
    )
    response = test_client.post('/books', json=new_book.model_dump(mode='json'))
    json_book: BookResponse = BookResponse.model_validate(response.json())

    assert response.status_code == 201
    assert json_book.title == 'Test'
    assert json_book.author == 'Test Author'
    assert json_book.id == 1


def test_get_book_by_id(test_client, db_session):
    new_book: CreateBookRequest = CreateBookRequest(
        title='Test',
        author='Test Author',
        edition=1,
        release_date=datetime(2020, 1, 1),
        publisher='Test Publisher',
        cover_img_url='http://cover.jpg',
        isbn_10='0123456789',
        isbn_13='0123456789123',
    )
    book: Book = BookService(db_session).create(new_book)

    response = test_client.get(f'/books/get/{book.id}')
    assert response.status_code == 200
