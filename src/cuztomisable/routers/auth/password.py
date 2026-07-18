from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from cuztomisable.db.models.users.passwords.reset import UserPasswordReset
from cuztomisable.exceptions import CuztomisableException
from cuztomisable.helpers.dependencies import get_db
from cuztomisable.lang import trans
from cuztomisable.schemas.message import MessageResponse
from cuztomisable.schemas.password import ForgotPasswordRequest, ForgotPasswordResponse, ResetPasswordRequest
from cuztomisable.schemas.users.tokens.access import TokenResponse
from cuztomisable.helpers.security import hash_password
from cuztomisable.services.users.auth import AuthService
from cuztomisable.services.users.passwords.password import UserPasswordService
from cuztomisable.services.users.passwords.reset import UserPasswordResetService
from cuztomisable.services.users.tokens.access import UserAccessTokenService
from cuztomisable.services.users.tokens.refresh import UserRefreshTokenService
from cuztomisable.settings import settings

router = APIRouter(prefix="/password/forgot", tags=["Password"])

# Caps how many wrong codes can be tried against a single token before it's
# burned outright — otherwise the code is just a short string someone could
# brute-force against a valid (unexpired, unused) token.
_MAX_CODE_ATTEMPTS = 5


def _register_failed_attempt(db: Session, record: UserPasswordReset) -> None:
    record.attempt_counter += 1
    if record.attempt_counter >= _MAX_CODE_ATTEMPTS:
        record.used_at = datetime.now(timezone.utc)
    db.commit()


@router.post("", response_model=ForgotPasswordResponse)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = AuthService(db).find_by_login_type(data.type or "email", data.username)
    now = datetime.now(timezone.utc)
    message = trans("password.forgot.success")
    if not user:
        return ForgotPasswordResponse(message=message)
    # Checks to see if the user has an existing, unexpired, unused reset token
    record = UserPasswordResetService(db).get_lastest_by_user(user.id)
    if record and not record.used_at and record.expires_at > now:
        last_created = now - timedelta(seconds=settings.forgot["time_between_allowed_resets"])
        if record.created_at > last_created:
            return ForgotPasswordResponse(
                message=trans("password.forgot.errors.sent_recently")
            )
    else:
        record = UserPasswordResetService(db).create(user.id)
        # Sends the email with the reset link
        UserPasswordResetService(db).send_email(user, record)
    return ForgotPasswordResponse(message=message, token=record.token)


@router.get("/{token}/send", response_model=MessageResponse)
def resend(token: str, db: Session = Depends(get_db)):
    record = UserPasswordResetService(db).get_by_token(token)
    if not record or record.used_at:
        raise CuztomisableException(
            code=status.HTTP_400_BAD_REQUEST,
            detail=trans("password.errors.invalid_reset_token"),
            exception="HTTPException",
            key="invalid_reset_token",
        )
    record.sent_at = datetime.now(timezone.utc)
    db.commit()
    return MessageResponse(message=trans("password.forgot.resent"))


@router.get("/{token}/verify", response_model=MessageResponse)
@router.get("/{token}/verify/{code}", response_model=MessageResponse)
def verify(
    token: str,
    code: Optional[str] = None,
    db: Session = Depends(get_db)
):
    record = UserPasswordResetService(db).get_by_token(token)

    invalid = CuztomisableException(
        code=status.HTTP_400_BAD_REQUEST,
        detail=trans("password.errors.invalid_reset_token"),
        exception="HTTPException",
        key="invalid_reset_token",
    )
    if not record or record.used_at:
        raise invalid
    if record.expires_at and record.expires_at < datetime.now(timezone.utc):
        raise invalid
    if code and record.code != code:
        _register_failed_attempt(db, record)
        raise invalid

    return MessageResponse(message=trans("password.forgot.valid"))


@router.post("/{token}", response_model=TokenResponse)
def reset(token: str, data: ResetPasswordRequest, request: Request, db: Session = Depends(get_db)):
    request.state.error_parameters = {"token": token}

    record = UserPasswordResetService(db).get_by_token(token)

    invalid = CuztomisableException(
        code=status.HTTP_400_BAD_REQUEST,
        detail=trans("password.errors.invalid_reset_token"),
        exception="HTTPException",
        key="invalid_reset_token",
    )
    if not record or record.used_at:
        raise invalid
    if record.expires_at and record.expires_at < datetime.now(timezone.utc):
        raise invalid
    if record.code != data.code:
        _register_failed_attempt(db, record)
        raise invalid

    user = record.user
    password_service = UserPasswordService(db)
    if password_service.is_reused(user.id, data.password):
        raise CuztomisableException(
            code=status.HTTP_400_BAD_REQUEST,
            detail=trans("validation.errors.password_recently_used"),
            exception="HTTPException",
            key="password_recently_used",
        )

    # Archive the outgoing hash before overwriting it
    password_service.create(user.id, {"password": user.password})
    user.password = hash_password(data.password)
    record.used_at = datetime.now(timezone.utc)

    # A password reset should kill every other existing session
    UserRefreshTokenService(db).revoke_all_for_user(user.id)
    UserAccessTokenService(db).revoke_all_for_user(user.id)

    access_token, access_record = UserAccessTokenService(db).create(user.id)
    refresh_record = UserRefreshTokenService(db).create(user.id)
    db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_record.token,
        expires_at=access_record.expires_at,
        message=trans("password.forgot.reset_success"),
    )
