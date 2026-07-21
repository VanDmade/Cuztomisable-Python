import uuid
from typing import Optional

from sqlalchemy.orm import Session

from cuztomisable.db.models.users.user import User
from cuztomisable.helpers.security import hash_password
from cuztomisable.helpers import generate_token
from cuztomisable.services.mail import MailService
from cuztomisable.settings import settings


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

    def send_verification_email(self, user: User) -> None:
        link = f"https://{settings.app_domain}/api/{user.token}/v/{user.email}"
        MailService(self.db).send_template(
            user.email,
            "email_verification",
            {"link": link},
            created_by=user.id,
        )

    def send_welcome_email(self, user: User) -> None:
        MailService(self.db).send_template(
            user.email,
            "new_registration",
            {"name": user.name},
            created_by=user.id,
        )

    def delete(self, user_id: uuid.UUID):
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.flush()
