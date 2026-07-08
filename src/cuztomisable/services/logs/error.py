import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from cuztomisable.db.models.logs.error import ErrorLog


class ErrorLogService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[ErrorLog]:
        return self.db.query(ErrorLog).order_by(ErrorLog.created_at.desc()).all()

    def get_by_user(self, user_id: uuid.UUID) -> List[ErrorLog]:
        return self.db.query(ErrorLog).filter(ErrorLog.user_id == user_id).all()

    def get_by_debug_code(self, debug_code: str) -> Optional[ErrorLog]:
        return self.db.query(ErrorLog).filter(ErrorLog.debug_code == debug_code).first()

    def create(self, data: dict) -> ErrorLog:
        record = ErrorLog(**data)
        self.db.add(record)
        self.db.flush()
        return record
