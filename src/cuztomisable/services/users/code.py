import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session

from cuztomisable.db.models.users.code import UserCode
from cuztomisable.helpers import generate_token
from cuztomisable.services.mail import MailService
from cuztomisable.settings import settings

_CODE_EXPIRY = timedelta(seconds=settings("multi_factor_authentication.code.expires_after", 300))


class UserCodeService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user(self, user_id: uuid.UUID) -> Optional[UserCode]:
        return self.db.query(UserCode).filter(UserCode.user_id == user_id).first()

    def get_by_code(self, code: str) -> Optional[UserCode]:
        return self.db.query(UserCode).filter(UserCode.code == code).first()

    def get_by_token(self, token: str) -> Optional[UserCode]:
        return self.db.query(UserCode).filter(UserCode.token == token).first()

    def create(self, user_id: uuid.UUID, data: dict) -> UserCode:
        code_settings = settings("multi_factor_authentication.code", {})
        record = UserCode(
            user_id=user_id,
            code=generate_token(
                length=settings("multi_factor_authentication.code.length", 6),
                characters=settings("multi_factor_authentication.code.characters", "0123456789"),
            ),
            token=secrets.token_hex(32),
            expires_at=datetime.now(timezone.utc) + _CODE_EXPIRY,
            **data,
        )
        self.db.add(record)
        self.db.flush()
        return record

    def send_email(self, user, record: UserCode) -> None:
        MailService(self.db).send_template(
            user.email,
            "mfa_code",
            {"code": record.code},
            created_by=user.id,
        )

    def delete(self, code_id: uuid.UUID):
        self.db.query(UserCode).filter(UserCode.id == code_id).delete()
        self.db.flush()

    def delete_all_by_user(self, user_id: uuid.UUID):
        self.db.query(UserCode).filter(UserCode.user_id == user_id).delete()
        self.db.flush()
