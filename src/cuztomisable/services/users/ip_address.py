import hashlib
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import Request
from sqlalchemy.orm import Session

from cuztomisable.db.models.users.ip_address import UserIpAddress


def _make_fingerprint(request: Request) -> str:
    user_agent = request.headers.get("User-Agent", "")
    platform = request.headers.get("X-App-Platform", "")
    raw = f"{user_agent}|{platform}".strip()
    return hashlib.sha256(raw.encode()).hexdigest() if raw else ""


class UserIpAddressService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user(self, user_id: uuid.UUID):
        pass

    def find_by_ip(self, user_id: uuid.UUID, request: Request) -> Optional[UserIpAddress]:
        ip_address = self.ip(request)
        if not ip_address:
            return None
        return (
            self.db.query(UserIpAddress)
            .filter_by(user_id=user_id, ip_address=ip_address)
            .first()
        )
    
    def find_or_create(self, user_id: uuid.UUID, request: Request) -> Optional[UserIpAddress]:
        record = self.find_by_ip(user_id, request)
        if not record:
            record = self.create(user_id, request)
        return record

    def create(self, user_id: uuid.UUID, request: Request) -> Optional[UserIpAddress]:
        ip_address = self.ip(request)
        if not ip_address:
            return None
        record = UserIpAddress(
            user_id=user_id,
            ip_address=ip_address,
            fingerprint=_make_fingerprint(request),
            last_used_at=datetime.now(timezone.utc),
        )
        self.db.add(record)
        self.db.flush()
        return record

    def delete(self, ip_address_id: uuid.UUID):
        pass

    def ip(self, request: Request) -> Optional[str]:
        return request.client.host if request.client else None