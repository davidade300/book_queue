from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from book_queue.core.database import DBHandler
from book_queue.core.settings import Settings
from book_queue.models.models import Base


def test_dbhandler_creates_and_closes_session():
    engine = create_engine(Settings.TEST_DATABASE_URL)
    Base.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine)

    db_handler = DBHandler(engine, session_factory)

    db_session = db_handler.get_session()
    yielded_session = next(db_session)

    assert yielded_session.is_active

    db_session.close()
    db_handler.engine.dispose()
