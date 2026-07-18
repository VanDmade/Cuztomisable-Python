from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from cuztomisable.exceptions import CuztomisableException
from cuztomisable.helpers.dependencies import get_db
from cuztomisable.lang import trans
from cuztomisable.schemas.login import LoginRequest
from cuztomisable.schemas.users.tokens.access import TokenResponse
from cuztomisable.schemas.users.user import UserResponse
from cuztomisable.helpers.security import verify_password
from cuztomisable.services.users.auth import AuthService
from cuztomisable.services.users.ip_address import UserIpAddressService
from cuztomisable.services.users.code import UserCodeService
from cuztomisable.services.users.tokens.access import UserAccessTokenService
from cuztomisable.services.users.tokens.refresh import UserRefreshTokenService
from cuztomisable.settings import settings

router = APIRouter(tags=["Login"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = AuthService(db).find_by_login_type(data.type, data.username)
    unauthorized = CuztomisableException(
        code=status.HTTP_401_UNAUTHORIZED,
        detail=trans("global.errors.invalid_credentials"),
        exception="HTTPException",
        key="invalid_credentials",
    )
    if not user:
        raise unauthorized
    if user.locked:
        raise CuztomisableException(
            code=status.HTTP_401_UNAUTHORIZED,
            detail=trans("global.errors.account_locked"),
            exception="HTTPException",
            key="account_locked",
        )
    now = datetime.now()
    if not verify_password(data.password, user.password):
        # Prevents brute-force attacks by locking the user out
        if user.attempt_counter > settings("login.max_attempts", 5):
            if settings("login.lock_on_max_attempts", False):
                user.locked = True
            user.attempt_timer = now + timedelta(seconds=settings("login.lock_time", 300))
            user.attempt_counter = 0
    # Checks the attempt timer
    if user.attempt_timer and user.attempt_timer > now:
        raise CuztomisableException(
            code=status.HTTP_401_UNAUTHORIZED,
            detail=trans("login.errors.too_many_attempts"),
            exception="HTTPException",
            key="too_many_attempts",
        )
    user.attempt_timer = None
    user.attempt_counter = 0
    db.commit()
    # Updates the timezone if it's provided
    if data.timezone and user.timezone != data.timezone:
        user.timezone = data.timezone
    # Finds the IP address record or creates a new one
    ip_address_record = UserIpAddressService(db).find_or_create(user.id, request)
    if ip_address_record:
        ip_address_record.last_used_at = now
        if user.multi_factor_authentication:
            if not ip_address_record.remember or ip_address_record.remember_until <= now:
                UserCodeService(db).delete_all_by_user(user.id)
                # Creates the token and code for user codes
                code_record = UserCodeService(db).create(
                    user_id=user.id,
                    user_ip_address_id=ip_address_record.id
                )
                # Sends the user to MFA instead of logging them in
                return MessageResponse(
                    message=trans("login.blah"),
                    redirect="mfa",
                    token=code_record.token,
                )
    db.commit()
    access_token, access_record = UserAccessTokenService(db).create(user.id)
    refresh_record = UserRefreshTokenService(db).create(user.id)
    db.commit()
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_record.token,
        expires_at=access_record.expires_at,
        user=UserResponse.model_validate(user).model_dump(mode="json"),
    )
