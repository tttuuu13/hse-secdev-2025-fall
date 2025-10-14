from sqlalchemy.orm import Session

from .. import schemas
from ..adapters import db_repository
from ..domain import models
from ..shared.errors import ConflictError


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: schemas.UserCreate) -> models.User:
        db_user = db_repository.get_user_by_email(self.db, email=user.email)
        if db_user:
            raise ConflictError("Email already registered")
        return db_repository.create_user(self.db, user=user)
