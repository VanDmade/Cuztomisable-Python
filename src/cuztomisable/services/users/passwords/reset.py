import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from cuztomisable.helpers.security import generate_token
from sqlalchemy.orm import Session

from cuztomisable.db.models.users.passwords.reset import UserPasswordReset
from cuztomisable.services.mail import MailService
from cuztomisable.settings import settings


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

    def get_by_code(self, code: str) -> Optional[UserPasswordReset]:
        return self.db.query(UserPasswordReset).filter(UserPasswordReset.code == code).first()

    def create(self, user_id: uuid.UUID) -> UserPasswordReset:
        expires_after = settings("reset_password.expires_after", 300)
        record = UserPasswordReset(
            user_id=user_id,
            code=generate_token(
                length=settings("reset_password.code.length", 6),
                characters=settings("reset_password.code.characters", "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            ),
            expires_at=datetime.now(timezone.utc) + timedelta(seconds=expires_after),
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
        link = f"https://{settings.app_domain}/password/reset/{record.code}"
        MailService(self.db).send_template(
            user.email,
            "reset_password",
            {"link": link, "code": record.code},
            created_by=user.id,
        )

    def send_sms(self, user, record: UserPasswordReset) -> None:
        pass