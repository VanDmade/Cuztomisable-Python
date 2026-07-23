from datetime import datetime, timedelta, timezone

from cuztomisable.schemas.message import MessageResponse
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from typing import Union

from typing import Optional

from cuztomisable.db.models.users.passwords.reset import UserPasswordReset
from cuztomisable.exceptions import CuztomisableException
from cuztomisable.helpers.dependencies import get_db
from cuztomisable.lang import trans
from cuztomisable.schemas.auth.password import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ForgotPasswordSendRequest,
    ResetPasswordRequest,
    VerifyResetCodeQuery,
)
from cuztomisable.schemas.redirect import RedirectMessageResponse
from cuztomisable.schemas.auth.tokens import TokenResponse
from cuztomisable.helpers.security import hash_password
from cuztomisable.services.users.auth import AuthService
from cuztomisable.services.users.passwords.password import UserPasswordService
from cuztomisable.services.users.passwords.reset import UserPasswordResetService
from cuztomisable.services.users.tokens.access import UserAccessTokenService
from cuztomisable.services.users.tokens.refresh import UserRefreshTokenService
from cuztomisable.settings import settings

router = APIRouter(prefix="/password/forgot", tags=["Password"])


def _invalid_code() -> CuztomisableException:
    return CuztomisableException(
        code=status.HTTP_400_BAD_REQUEST,
        message=trans("password.errors.invalid_reset_code"),
        key="invalid_reset_code",
    )

def _code_expired() -> CuztomisableException:
    return CuztomisableException(
        code=status.HTTP_400_BAD_REQUEST,
        message=trans("password.errors.reset_code_expired"),
        key="reset_code_expired",
        parameters={"redirect_url": "/password/forgot"},
    )

def _recently_expired(record: UserPasswordReset) -> bool:
    if not record.expires_at:
        return False
    recently_expired_window = settings("password.forgot.recently_expired_window", 60)
    return record.expires_at < datetime.now(timezone.utc) and record.expires_at > datetime.now(timezone.utc) - timedelta(seconds=recently_expired_window)


def _validate_record(record: Optional[UserPasswordReset]) -> bool:
    recently_expired = _recently_expired(record) if record else False
    if record is None or record.used_at or (record.expires_at < datetime.now(timezone.utc) and not recently_expired):
        return False
    if recently_expired:
        raise _code_expired()
    return True


@router.post("",
    response_model=RedirectMessageResponse,
    response_model_exclude_none=True
)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = AuthService(db).find_by_login_type(data.type or "email", data.username)
    now = datetime.now(timezone.utc)
    message = trans("password.forgot.success")
    redirect_url = f"/password/reset?username={data.username}"
    if not user:
        # User doesn't exist and we don't want to give away info for free
        return RedirectMessageResponse(
            message=message,
            url=redirect_url,
        )
    resetService = UserPasswordResetService(db)
    # Checks to see if the user has an existing, unexpired, unused reset code
    record = resetService.get_lastest_by_user(user.id)
    if record and not record.used_at and record.expires_at > now:
        last_created = now - timedelta(seconds=settings("reset_password.resend_timer", 60))
        if record.created_at > last_created:
            return RedirectMessageResponse(
                message=trans("password.forgot.errors.sent_recently"),
                url=redirect_url,
            )
    else:
        record = resetService.create(user.id)
        if data.type == "phone":
            # Sends the SMS with the reset code
            resetService.send_sms(user, record)
        else:
            # Sends the email with the reset code
            resetService.send_email(user, record)
        # Marks the record as sent and how it was sent
        record.sent_at = datetime.now(timezone.utc)
        record.sent_via = data.type
        db.commit()
    return RedirectMessageResponse(
        message=message,
        url=redirect_url,
    )


@router.post("/send", response_model=MessageResponse)
def send_code(data: ForgotPasswordSendRequest, db: Session = Depends(get_db)):
    user = AuthService(db).find_by_login_type(data.type, data.username)
    success_response = MessageResponse(message=trans("password.resent"))
    if not user:
        raise _invalid_code()
    record = UserPasswordResetService(db).get_lastest_by_user(user.id)
    # Checks for a record, if it doesn't exist then leave the user here
    if not _validate_record(record):
        return success_response
    resend_timer = settings("password.forgot.resend_timer", 60)
    if record.sent_at and record.sent_at > datetime.now(timezone.utc) - timedelta(seconds=resend_timer):
        raise CuztomisableException(
            code=status.HTTP_400_BAD_REQUEST,
            message=trans("password.errors.code_sent_too_recently"),
            key="code_sent_too_recently",
        )
    if settings("password.forgot.code.regenerate_on_resend", False):
        record.code = UserPasswordResetService(db).generate_code()
    if data.type == "email" and user.email and settings("password.forgot.with.email", True):
        UserPasswordResetService(db).send_email(user, record)
    elif data.type == "sms" and user.phone and settings("password.forgot.with.phone", True):
        # TODO :: Implement SMS sending logic here
        pass
    record.sent_at = datetime.now(timezone.utc)
    record.sent_via = data.type
    db.commit()
    return success_response


@router.get("/{code}/verify", response_model=ForgotPasswordResponse)
def verify(
    code: str,
    query: VerifyResetCodeQuery = Depends(),
    db: Session = Depends(get_db),
):
    user = AuthService(db).find_by_login_type(query.type, query.username)
    record = UserPasswordResetService(db).get_by_code(code)
    if not user or not record or record.user_id != user.id:
        raise _invalid_code()
    if not _validate_record(record):
        raise _invalid_code()
    return ForgotPasswordResponse(
        message=trans("password.forgot.valid"),
        username=query.username
    )


@router.post("/", 
    response_model=Union[TokenResponse, RedirectMessageResponse],
    response_model_exclude_none=True
)
def reset(
    data: ResetPasswordRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    request.state.error_parameters = {"code": data.code, "username": data.username}
    user = AuthService(db).find_by_login_type(data.type, data.username)
    record = UserPasswordResetService(db).get_by_code(data.code)
    if not user or not record or record.user_id != user.id:
        raise _invalid_code()
    if not _validate_record(record):
        raise _invalid_code()
    if record.code != data.code:
        record.attempt_counter += 1
        if record.attempt_counter >= settings("reset_password.max_attempts", 5):
            # Marks it as used so the user can't keep trying to guess it
            record.used_at = datetime.now(timezone.utc)
            db.commit()
            raise CuztomisableException(
                code=status.HTTP_400_BAD_REQUEST,
                message=trans("password.errors.reset_code_max_attempts"),
                key="reset_code_max_attempts",
            )
    password_service = UserPasswordService(db)
    if password_service.is_reused(user.id, data.password):
        raise CuztomisableException(
            code=status.HTTP_400_BAD_REQUEST,
            message=trans("validation.errors.password_recently_used"),
            key="password_recently_used",
        )
    user.password = hash_password(data.password)
    # Archive the outgoing hash before overwriting it
    password_service.create(user.id, {"password": user.password})
    record.used_at = datetime.now(timezone.utc)
    if settings("reset_password.on_change_clear_sessions", True):
        # A password reset should kill every other existing session
        UserRefreshTokenService(db).revoke_all_for_user(user.id)
        UserAccessTokenService(db).revoke_all_for_user(user.id)
    message = trans("password.reset.success")
    if not settings("reset_password.login_after", False):
        # The developer doesn't want the user logging in automatically
        db.commit()
        return RedirectMessageResponse(
            message=message,
            url="/login",
        )
    access_token, access_record = UserAccessTokenService(db).create(user.id)
    refresh_record = UserRefreshTokenService(db).create(user.id)
    db.commit()
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_record.token,
        expires_at=access_record.expires_at,
        message=message,
    )
