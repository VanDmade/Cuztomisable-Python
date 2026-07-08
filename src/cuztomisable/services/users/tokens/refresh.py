import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session

from cuztomisable.db.models.users.tokens.refresh import UserRefreshToken
from cuztomisable.settings import settings


class UserRefreshTokenService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: uuid.UUID) -> UserRefreshToken:
        token_str = secrets.token_urlsafe(48)
        expire = timedelta(days=settings.refresh_token_expire_days)
        expires_at = datetime.now(timezone.utc) + expire
        record = UserRefreshToken(
            user_id=user_id,
            token=token_str,
            expires_at=expires_at
        )
        self.db.add(record)
        self.db.flush()
        return record

    def validate(self, token: str) -> Optional[UserRefreshToken]:
        record = (
            self.db.query(UserRefreshToken)
                .filter(
                    UserRefreshToken.token == token,
                    UserRefreshToken.revoked == False,
                )
                .first()
        )
        # The record does not exist or has been revoked
        if not record:
            return None
        # The record has expired
        if record.expires_at and record.expires_at < datetime.now(timezone.utc):
            return None
        return record

    def get_by_user(self, user_id: uuid.UUID) -> list[UserRefreshToken]:
        return (
            self.db.query(UserRefreshToken)
                .filter(
                    UserRefreshToken.user_id == user_id,
                    UserRefreshToken.revoked == False
                )
                .all()
        )

    def get_by_token(self, token: str) -> Optional[UserRefreshToken]:
        return (
            self.db.query(UserRefreshToken)
                .filter(UserRefreshToken.token == token)
                .first()
        )

    def revoke(self, token_id: uuid.UUID) -> bool:
        record = (
            self.db.query(UserRefreshToken)
                .filter(UserRefreshToken.id == token_id)
                .first()
        )
        # The record does not exist or has been revoked
        if not record:
            return False
        record.revoked = True
        self.db.commit()
        return True

    def revoke_all_for_user(self, user_id: uuid.UUID) -> None:
        (
            self.db.query(UserRefreshToken)
                .filter(
                    UserRefreshToken.user_id == user_id,
                    UserRefreshToken.revoked == False,
                )
                .update({"revoked": True})
        )
        self.db.commit()

    def delete(self, token_id: uuid.UUID) -> bool:
        record = (
            self.db.query(UserRefreshToken)
                .filter(UserRefreshToken.id == token_id)
                .first()
        )
        # The record does not exist or has been revoked
        if not record:
            return False
        self.db.delete(record)
        self.db.commit()
        return True
