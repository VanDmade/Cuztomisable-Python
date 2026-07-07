import uuid
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from cuztomisable.context import current_user_id
from cuztomisable.db.models.users.tokens.access import UserAccessToken
from cuztomisable.db.models.users.user import User
from cuztomisable.lang import trans
from cuztomisable.settings import settings

_SessionLocal = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")


def configure_db(session_local) -> None:
    global _SessionLocal
    _SessionLocal = session_local


def get_db() -> Generator[Session, None, None]:
    if _SessionLocal is None:
        raise RuntimeError(trans("global.errors.database_not_configured"))
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=trans("global.errors.invalid_or_expired_token"),
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise unauthorized
    jti = payload.get("jti")
    user_id = payload.get("sub")
    # If either jti or user_id is missing, raise an unauthorized exception
    if not jti or not user_id:
        raise unauthorized
    record = (
        db.query(UserAccessToken)
            .filter(
                UserAccessToken.token == jti,
                UserAccessToken.revoked == False,
            )
            .first()
    )
    if not record:
        raise unauthorized
    user = db.query(User).filter(User.id == uuid.UUID(user_id)).first()
    if not user or user.locked:
        raise unauthorized
    current_user_id.set(user.id)
    return user
