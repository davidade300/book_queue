from sqlalchemy import (
    select,
)
from sqlalchemy.orm import Session

from book_queue.core.schemas import CreateUserRequest
from book_queue.core.security import get_password_hash
from book_queue.models.models import User


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, data: CreateUserRequest):
        user: User = User.create(
            data.username, data.password, password_hasher=get_password_hash
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

    def get_user(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        user: User | None = self.db.execute(stmt).scalar_one_or_none()
        return user
