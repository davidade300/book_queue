from datetime import datetime

from book_queue.models.models import Book
from book_queue.schemas import CreateBookRequest


def test_create_book(
    book_service,
):
    book_request: CreateBookRequest = CreateBookRequest(
        title='test book',
        author='test author',
        edition=1,
        release_date=datetime.now(),
        isbn_10='1234567890',
        isbn_13='1234567890123',
        publisher='test publisher',
        cover_img_url='https://example.com',
    )
    test_book = book_service.create(book_request)

    assert test_book.title == 'test book'


def test_get_book_by_id(book_service, instantiate_models_and_populate_db):
    b, _, _, _, _ = instantiate_models_and_populate_db

    book_in_db: Book = book_service.get_by_id(b.id)

    assert book_in_db.title == b.title
    assert book_in_db.id == b.id


def test_list_books(book_service, instantiate_models_and_populate_db):
    b, _, _, _, _ = instantiate_models_and_populate_db
    books: list[Book] = book_service.list_books()

    assert len(books) == 1
    assert books[0].title == b.title


def test_delete_book(book_service, instantiate_models_and_populate_db):
    b, _, _, _, _ = instantiate_models_and_populate_db

    deleted_book: Book = book_service.delete(b.id)

    assert deleted_book is None
