from sqlalchemy.orm import Session

from book_queue.core import security
from book_queue.core.security import DUMMY_HASH
from book_queue.models.models import User
from book_queue.services.user_service import UserService


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, username: str, password: str) -> User | None:

        user: User | None = UserService(self.db).get_user(username)
        if not user:
            security.verify_password(password, DUMMY_HASH)
            return None
        if not security.verify_password(password, user.hashed_password):
            return None
        return user
