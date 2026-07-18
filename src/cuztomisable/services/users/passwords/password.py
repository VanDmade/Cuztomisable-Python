import uuid
from typing import List

from sqlalchemy.orm import Session

from cuztomisable.db.models.users.passwords.password import UserPassword
from cuztomisable.helpers.security import verify_password
from cuztomisable.settings import settings


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
        self.db.flush()
        return record

    def is_reused(self, user_id: uuid.UUID, plain_password: str) -> bool:
        limit = settings.reuse_password_after or None
        if not limit:
            return False
        history = self.get_by_user(user_id)[:limit]
        return any(verify_password(plain_password, record.password) for record in history)

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
