from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from book_queue.models.models import Book
from book_queue.core.schemas import CreateBookRequest


class BookService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: CreateBookRequest) -> Book:
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
        stmt = select(Book).where(Book.id == book_id)
        book: Book = self.db.execute(stmt).scalar_one()
        self.db.commit()

        return book

    def list_books(self) -> list[Book]:
        stmt = select(Book).order_by(Book.created_at.desc())
        books: list[Book] = list[Book](self.db.execute(stmt).scalars().all())

        return books

    def delete(self, book_id: int) -> None:
        book: Book = self.get_by_id(book_id)

        self.db.delete(book)
        self.db.commit()
