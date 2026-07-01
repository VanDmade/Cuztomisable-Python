import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from sqlalchemy.orm import Session

from cuztomisable.db.models.users.tokens.access import UserAccessToken
from cuztomisable.settings import settings


class UserAccessTokenService:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: uuid.UUID) -> tuple[str, UserAccessToken]:
        jti = str(uuid.uuid4())
        expire = timedelta(minutes=settings.access_token_expire_minutes)
        expires_at = datetime.now(timezone.utc) + expire
        # Create the JWT token with the user_id and jti as payload
        payload = {
            # Subject — the user this token belongs to
            "sub": str(user_id),
            # JWT ID — unique identifier for revocation lookup
            "jti": jti,
            # Expiry — automatically validated on decode
            "exp": expires_at,
        }
        # Encode the JWT token using the secret and algorithm from settings
        token_str = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )
        record = UserAccessToken(
            user_id=user_id,
            token=jti,
            expires_at=expires_at
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return token_str, record

    def validate(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )
        except JWTError:
            return None
        jti = payload.get("jti")
        record = (
            self.db.query(UserAccessToken)
                .filter(
                    UserAccessToken.token == jti,
                    UserAccessToken.revoked == False,
                )
                .first()
        )
        # The record does not exist or has been revoked
        if not record:
            return None
        return payload

    def get_by_user(self, user_id: uuid.UUID) -> list[UserAccessToken]:
        return (
            self.db.query(UserAccessToken)
                .filter(
                    UserAccessToken.user_id == user_id,
                    UserAccessToken.revoked == False,
                )
                .all()
        )

    def get_by_token(self, token: str) -> Optional[UserAccessToken]:
        record = (
            self.db.query(UserAccessToken)
                .filter(UserAccessToken.token == token)
                .first()
        )
        # The record does not exist or has been revoked
        if not record:
            return None
        return record

    def revoke(self, token_id: uuid.UUID) -> bool:
        record = (
            self.db.query(UserAccessToken)
                .filter(UserAccessToken.id == token_id)
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
            self.db.query(UserAccessToken)
                .filter(
                    UserAccessToken.user_id == user_id,
                    UserAccessToken.revoked == False,
                )
                .update({"revoked": True})
        )
        self.db.commit()

    def delete(self, token_id: uuid.UUID) -> bool:
        record = (
            self.db.query(UserAccessToken)
                .filter(UserAccessToken.id == token_id)
                .first()
        )
        # The record does not exist or has been revoked
        if not record:
            return False
        self.db.delete(record)
        self.db.commit()
        return True
