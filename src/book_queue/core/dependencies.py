from typing import Generator

from sqlalchemy.orm import Session

from book_queue.core.database import DBHandler, SessionLocal, engine

db_handler = DBHandler(engine, SessionLocal)


def get_db() -> Generator[Session]:
    yield from db_handler.get_session()
