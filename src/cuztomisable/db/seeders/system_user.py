import uuid

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from cuztomisable.db.models.users.user import User
from cuztomisable.settings import settings

SYSTEM_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000000")

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed_system_user(db: Session) -> None:
    existing = db.query(User).filter(User.id == SYSTEM_USER_ID).first()

    if existing:
        return

    system_user = User(
        id=SYSTEM_USER_ID,
        name="System",
        email=f"system@{settings.app_domain}",
        password=_pwd_context.hash("password"),
        admin=True,
        locked=False,
        change_password=True
    )

    db.add(system_user)
    db.commit()
