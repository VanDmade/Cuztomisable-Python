import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session

from cuztomisable.db.models.users.code import UserCode

_CODE_EXPIRY = timedelta(hours=24)


class UserCodeService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user(self, user_id: uuid.UUID):
        pass

    def get_by_code(self, code: str) -> Optional[UserCode]:
        return self.db.query(UserCode).filter(UserCode.code == code).first()

    def create(self, user_id: uuid.UUID, data: dict) -> UserCode:
        record = UserCode(
            user_id=user_id,
            code=secrets.token_hex(8),
            sent_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + _CODE_EXPIRY,
            **data,
        )
        self.db.add(record)
        self.db.flush()
        return record

    def delete(self, code_id: uuid.UUID):
        self.db.query(UserCode).filter(UserCode.id == code_id).delete()
        self.db.flush()

    def delete_all_by_user(self, user_id: uuid.UUID):
        self.db.query(UserCode).filter(UserCode.user_id == user_id).delete()
        self.db.flush()
