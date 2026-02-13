from datetime import datetime
from typing import Generator

import pytest
from sqlalchemy import Connection, Engine, create_engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from book_queue.core.dependencies import db_dependecy
from book_queue.core.settings import Settings
from book_queue.main import app
from book_queue.models.models import Base, Book, Chapter, Note
from book_queue.services.book_service import BookService
from book_queue.services.chapter_service import ChapterService
from book_queue.services.notes_service import NoteService


@pytest.fixture(scope='function')
def db_session() -> Generator[Session]:
    engine: Engine = create_engine(url=Settings.TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    connection: Connection = engine.connect()
    session: Session = Session(bind=connection)

    try:
        yield session
    finally:
        session.close()
        connection.close()
        engine.dispose()


@pytest.fixture(scope='function')
def instantiate_models_and_populate_db(
    db_session: Session,
) -> tuple[Book, Chapter, Chapter, Note, Note]:
    book: Book = Book(
        title='Test Book',
        author='Test Author',
        edition=1,
        release_date=datetime(2026, 6, 2),
        publisher='Test Publisher',
        isbn_10='0-321-12742-0',
        isbn_13='978-0-321-12742-6',
        cover_img_url='test-cover.jpg',
    )

    chapter_1: Chapter = Chapter(
        title='Test Chapter 1',
    )
    chapter_2: Chapter = Chapter(
        title='Test Chapter 2',
    )

    note_1: Note = Note(
        title='Test Note 1',
        content='Test Note 1 Content',
    )

    note_2: Note = Note(
        title='Test Note 2',
        content='Test Note 2 Content',
    )

    chapter_1.notes.append(note_1)

    chapter_2.notes.append(note_2)

    book.chapters.append(chapter_1)
    book.chapters.append(chapter_2)

    db_session.add(instance=book)

    db_session.commit()

    return book, chapter_1, chapter_2, note_1, note_2


@pytest.fixture(scope='function')
def note_service(db_session):
    return NoteService(db=db_session)


@pytest.fixture(scope='function')
def chapter_service(db_session):
    return ChapterService(db=db_session)


@pytest.fixture(scope='function')
def book_service(db_session):
    return BookService(db=db_session)


@pytest.fixture(scope='function')
def test_client() -> TestClient:

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

        app.dependency_overrides[db_dependecy] = override_get_db

    return TestClient(app)
