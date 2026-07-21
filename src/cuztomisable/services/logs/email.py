import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from cuztomisable.db.models.logs.email import EmailLog
from cuztomisable.settings import settings


class EmailLogService:

    santize_keys = settings("email.sanitize_keys", [])

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[EmailLog]:
        return self.db.query(EmailLog).order_by(EmailLog.created_at.desc()).all()

    def get_by_user(self, user_id: uuid.UUID) -> List[EmailLog]:
        return self.db.query(EmailLog).filter(EmailLog.created_by == user_id).all()

    def create(self, user_id: Optional[uuid.UUID], data: dict) -> EmailLog:
        # Cleans the parameters and subject to remove passwords, codes, and tokens for cleaning
        data["parameters"] = self.clean_parameters(data.get("parameters", {}))
        record = EmailLog(created_by=user_id, **data)
        self.db.add(record)
        self.db.flush()
        return record

    def clean_parameters(self, parameters: dict) -> dict:
        cleaned = {}
        for key, value in parameters.items():
            if any(sanitize_key in key.lower() for sanitize_key in self.santize_keys):
                cleaned[key] = "[REDACTED]"
            else:
                cleaned[key] = value
        return cleaned
