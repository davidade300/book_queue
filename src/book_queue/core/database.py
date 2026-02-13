from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from book_queue.core.settings import Settings

engine: Engine = create_engine(
    url=Settings.DATABASE_URL,
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
