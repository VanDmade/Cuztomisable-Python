import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session

from cuztomisable.db.models.users.verification import UserVerification

_TOKEN_EXPIRY = timedelta(hours=24)


class UserVerificationService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_token(self, token: str) -> Optional[UserVerification]:
        return self.db.query(UserVerification).filter(UserVerification.token == token).first()

    def create(self, user_id: uuid.UUID, type: str) -> UserVerification:
        record = UserVerification(
            user_id=user_id,
            type=type,
            token=secrets.token_hex(4),
            sent_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + _TOKEN_EXPIRY,
        )
        self.db.add(record)
        self.db.flush()
        return record
