from typing import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from book_queue.core.settings import Settings

engine: Engine = create_engine(
    url=Settings.TEST_DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class DBHandler:
    """
    My aim with this class is that it acts similar to a Unity Of Work
    instead of using the plain old  get_db/get_session function pattern
    """
    def __init__(
        self, db_engine: Engine, session_factory: sessionmaker
    ) -> None:
        self.engine = db_engine
        self.session_factory = session_factory

    def get_session(self) -> Generator[Session]:
        db: Session = self.session_factory()
        try:
            yield db
        finally:
            db.close()
