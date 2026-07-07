from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from cuztomisable.db.models.phone import Phone
from cuztomisable.db.models.users.user import User
from cuztomisable.dependencies import get_db
from cuztomisable.lang import trans
from cuztomisable.schemas.login import LoginRequest
from cuztomisable.schemas.users.tokens.access import TokenResponse
from cuztomisable.services.users.tokens.access import UserAccessTokenService
from cuztomisable.services.users.tokens.refresh import UserRefreshTokenService

router = APIRouter(tags=["Login"])

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=trans("global.errors.invalid_credentials"),
    )

    user = None
    if data.type == "phone":
        phone = db.query(Phone).filter(Phone.number == data.username).first()
        user = phone.user if phone else None
    elif data.type == "username":
        user = db.query(User).filter(User.username == data.username).first()
    else:
        user = db.query(User).filter(User.email == data.username).first()

    if not user or not _pwd_context.verify(data.password, user.password):
        raise unauthorized
    if user.locked:
        raise unauthorized

    access_token, access_record = UserAccessTokenService(db).create(user.id)
    refresh_record = UserRefreshTokenService(db).create(user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_record.token,
        expires_at=access_record.expires_at,
    )
