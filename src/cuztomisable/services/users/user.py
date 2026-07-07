import uuid
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from cuztomisable.db.models.users.user import User

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        pass

    def get_by_id(self, user_id: uuid.UUID):
        pass

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, data: dict) -> User:
        data = dict(data)
        data["password"] = _pwd_context.hash(data["password"])
        user = User(**data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: uuid.UUID, data: dict):
        pass

    def delete(self, user_id: uuid.UUID):
        pass
