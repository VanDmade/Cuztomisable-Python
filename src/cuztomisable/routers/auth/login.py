from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Union
from cuztomisable.exceptions import CuztomisableException
from cuztomisable.helpers.dependencies import get_db
from cuztomisable.lang import trans
from cuztomisable.schemas.authentication import LoginRequest
from cuztomisable.schemas.redirect import RedirectMessageResponse
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


@router.post(
    "/login",
    response_model=Union[TokenResponse, RedirectMessageResponse],
    response_model_exclude_none=True
)
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = AuthService(db).find_by_login_type(data.type, data.username)
    unauthorized = CuztomisableException(
        code=status.HTTP_401_UNAUTHORIZED,
        message=trans("global.errors.invalid_credentials"),
        key="invalid_credentials",
    )
    attempt_timer = CuztomisableException(
        code=status.HTTP_401_UNAUTHORIZED,
        message=trans("login.errors.too_many_attempts"),
        key="too_many_attempts",
    )
    if not user:
        raise unauthorized
    if user.locked:
        raise CuztomisableException(
            code=status.HTTP_401_UNAUTHORIZED,
            message=trans("global.errors.account_locked"),
            key="account_locked",
        )
    now = datetime.now(timezone.utc)
    # Checks the attempt timer
    if user.attempt_timer and user.attempt_timer > now:
        raise attempt_timer
    valid_password = verify_password(data.password, user.password)
    if not valid_password:
        # Invalid password so we need to increment the attempt counter and continue
        user.attempts += 1
        # Prevents brute-force attacks by locking the user out
        if user.attempts >= settings("login.max_attempts", 5):
            if settings("login.lock_on_max_attempts", False):
                user.locked = True
            user.attempt_timer = now + timedelta(seconds=settings("login.attempt_timer", 300))
            user.attempts = 0
            db.commit()
            raise attempt_timer
        db.commit()
        raise unauthorized
    # Resets the counter if they successfully logged in
    user.attempt_timer = None
    user.attempts = 0
    db.commit()
    # Updates the timezone if it's provided
    if data.timezone and user.timezone != data.timezone:
        user.timezone = data.timezone
    # Finds the IP address record or creates a new one
    ip_address_record = UserIpAddressService(db).find_or_create(user.id, request)
    if ip_address_record:
        # Determines if the IP Address is new and whether or not to notify
        if (ip_address_record.last_used_at is None and
            settings("email.notify_on_new_ip_address", True)):
            UserIpAddressService(db).send_email(user, ip_address_record)
        ip_address_record.last_used_at = now
        if (user.multi_factor_authentication and
            settings("multi_factor_authentication.enabled", True)):
            if not ip_address_record.remember or ip_address_record.remember_until <= now:
                UserCodeService(db).delete_all_by_user(user.id)
                # Creates the token and code for user codes
                code_record = UserCodeService(db).create(
                    user_id=user.id,
                    data={"user_ip_address_id": ip_address_record.id}
                )
                db.commit()
                return RedirectMessageResponse(
                    message=trans("login.multi_factor_authentication.sent"),
                    url=f"/mfa/{code_record.token}",
                )
    access_token, access_record = UserAccessTokenService(db).create(user.id)
    refresh_record = UserRefreshTokenService(db).create(user.id)
    db.commit()
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_record.token,
        expires_at=access_record.expires_at,
        user=UserResponse.model_validate(user).model_dump(mode="json"),
    )
