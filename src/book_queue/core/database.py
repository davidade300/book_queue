from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from book_queue.core.settings import Settings
from book_queue.models.models import Base

engine: Engine = create_engine(
    url=Settings.TEST_DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
