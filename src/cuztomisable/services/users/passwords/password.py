import uuid
from typing import List

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from cuztomisable.db.models.users.passwords.password import UserPassword
from cuztomisable.db.models.users.user import User
from cuztomisable.settings import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserPasswordService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user(self, user_id: uuid.UUID) -> List[UserPassword]:
        return (
            self.db.query(UserPassword)
                .filter(UserPassword.user_id == user_id)
                .order_by(UserPassword.created_at.desc())
                .all()
        )

    def create(self, user_id: uuid.UUID, data: dict) -> UserPassword:
        record = UserPassword(user_id=user_id, **data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def is_reused(self, user_id: uuid.UUID, plain_password: str) -> bool:
        limit = settings.reuse_password_after
        if not limit:
            return False

        user = self.db.query(User).filter(User.id == user_id).first()
        if user and _pwd_context.verify(plain_password, user.password):
            return True

        history = self.get_by_user(user_id)[:limit]
        return any(_pwd_context.verify(plain_password, record.password) for record in history)

    def delete(self, password_id: uuid.UUID) -> bool:
        record = (
            self.db.query(UserPassword)
                .filter(UserPassword.id == password_id)
                .first()
        )
        if not record:
            return False
        self.db.delete(record)
        self.db.commit()
        return True
