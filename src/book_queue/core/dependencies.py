from fastapi import Depends
from sqlalchemy.orm import Session

from book_queue.core.database import get_db


db_dependecy: Session = Depends(get_db)