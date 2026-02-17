from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from book_queue.core.schemas import CreateBookRequest
from book_queue.models.models import Book


class BookService:
    """
    This class is a base service for the Book model
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: CreateBookRequest) -> Book:
        """
        Create a new book from a CreateBookRequest BaseModel.
        :param data: object of CreateBookRequest type
        :return: book:Book
        """
        stmt = (
            insert(Book)
            .values(
                **data.model_dump(
                    exclude_none=True,
                    exclude_unset=True,
                )
            )
            .returning(Book)
        )

        book: Book = self.db.execute(stmt).scalar_one()
        self.db.commit()

        return book

    def get_by_id(self, book_id: int) -> Book:
        """
        return a book by it's id
        :param book_id: int representing the id of the searched book
        :return: book:Book
        """
        stmt = select(Book).where(Book.id == book_id)
        book: Book = self.db.execute(stmt).scalar_one()

        return book

    def list_books(self) -> list[Book]:
        """
        return a list of all Books
        :return: list of Book
        """
        stmt = select(Book).order_by(Book.created_at.desc())
        books: list[Book] = list[Book](self.db.execute(stmt).scalars().all())

        return books

    def delete(self, book_id: int) -> None:
        """
        Delete a book by it's id
        :param book_id: int representing the id of the book to delete
        :return: None
        """
        book: Book = self.get_by_id(book_id)

        self.db.delete(book)
        self.db.commit()
