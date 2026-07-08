from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from cuztomisable.dependencies import get_db
from cuztomisable.lang import trans
from cuztomisable.schemas.login import LoginRequest
from cuztomisable.schemas.users.tokens.access import TokenResponse
from cuztomisable.security import verify_password
from cuztomisable.services.users.auth import AuthService
from cuztomisable.services.users.ip_address import UserIpAddressService
from cuztomisable.services.users.tokens.access import UserAccessTokenService
from cuztomisable.services.users.tokens.refresh import UserRefreshTokenService

router = APIRouter(tags=["Login"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=trans("global.errors.invalid_credentials"),
    )

    user = AuthService(db).find_by_login_type(data.type, data.username)

    if not user or not verify_password(data.password, user.password):
        raise unauthorized
    if user.locked:
        raise unauthorized

    if data.timezone and user.timezone != data.timezone:
        user.timezone = data.timezone

    UserIpAddressService(db).create(user.id, request)

    access_token, access_record = UserAccessTokenService(db).create(user.id)
    refresh_record = UserRefreshTokenService(db).create(user.id)
    db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_record.token,
        expires_at=access_record.expires_at,
    )
