from sqlalchemy import (
    false,
    select,
)
from sqlalchemy.orm import Session

from book_queue.core import security
from book_queue.core.schemas import CreateUserRequest
from book_queue.core.security import DUMMY_HASH, get_password_hash
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
        # self.db.refresh(user)

    def get_user(self, username: str) -> User:
        stmt = select(User).where(User.username == username)
        user: User = self.db.execute(stmt).scalar_one()

        return user

    def authenticate_user(self, username: str, password: str):

        user = self.get_user(username)
        if not user:
            security.verify_password(password, DUMMY_HASH)
            return false
        if not security.verify_password(password, user.hashed_password):
            return False
        return user
