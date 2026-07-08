from typing import Optional

from sqlalchemy.orm import Session

from cuztomisable.db.models.users.user import User


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def find_by_login_type(self, login_type: str, username: str) -> Optional[User]:
        query = self.db.query(User).filter(User.deleted_at.is_(None))
        if login_type == "phone":
            return query.filter(User.phone == username).first()
        if login_type == "username":
            return query.filter(User.username == username).first()
        return query.filter(User.email == username).first()
