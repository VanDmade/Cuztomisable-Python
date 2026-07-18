import uuid
from typing import Optional

from sqlalchemy.orm import Session

from cuztomisable.db.models.users.user import User
from cuztomisable.helpers.security import hash_password
from cuztomisable.helpers import generate_token


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        pass

    def get_by_id(self, user_id: uuid.UUID):
        pass

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_token(self, token: str) -> Optional[User]:
        return self.db.query(User).filter(User.token == token).first()

    def create(self, data: dict) -> User:
        data = dict(data)
        data["password"] = hash_password(data["password"])
        data["token"] = generate_token()
        user = User(**data)
        self.db.add(user)
        self.db.flush()
        return user

    def update(self, user_id: uuid.UUID, data: dict):
        pass

    def delete(self, user_id: uuid.UUID):
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.flush()
