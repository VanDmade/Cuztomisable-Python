import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from cuztomisable.db.models.users.passwords.reset import UserPasswordReset

_RESET_EXPIRY = timedelta(hours=1)


class UserPasswordResetService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user(self, user_id: uuid.UUID) -> List[UserPasswordReset]:
        return (
            self.db.query(UserPasswordReset)
                .filter(UserPasswordReset.user_id == user_id)
                .order_by(UserPasswordReset.created_at.desc())
                .all()
        )
    
    def get_lastest_by_user(self, user_id: uuid.UUID) -> Optional[UserPasswordReset]:
        return (
            self.db.query(UserPasswordReset)
                .filter(UserPasswordReset.user_id == user_id)
                .order_by(UserPasswordReset.created_at.desc())
                .first()
        )

    def get_by_token(self, token: str) -> Optional[UserPasswordReset]:
        return self.db.query(UserPasswordReset).filter(UserPasswordReset.token == token).first()

    def create(self, user_id: uuid.UUID) -> UserPasswordReset:
        record = UserPasswordReset(
            user_id=user_id,
            code=secrets.token_hex(4),
            token=secrets.token_hex(4),
            sent_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + _RESET_EXPIRY,
        )
        self.db.add(record)
        self.db.flush()
        return record

    def delete(self, reset_id: uuid.UUID) -> bool:
        record = (
            self.db.query(UserPasswordReset)
                .filter(UserPasswordReset.id == reset_id)
                .first()
        )
        if not record:
            return False
        self.db.delete(record)
        self.db.commit()
        return True

    def send_email(self, user, record: UserPasswordReset) -> None:
        # Placeholder for sending email logic
        pass