from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from cuztomisable.db.models.users.code import UserCode
from cuztomisable.exceptions import CuztomisableException
from cuztomisable.helpers.dependencies import get_db
from cuztomisable.helpers.maskers import mask_email, mask_phone
from cuztomisable.lang import trans
from cuztomisable.schemas.authentication import MfaChannelsResponse, MfaLoginRequest, MfaSendRequest
from cuztomisable.schemas.message import MessageResponse
from cuztomisable.schemas.users.tokens.access import TokenResponse
from cuztomisable.schemas.users.user import UserResponse
from cuztomisable.services.users.code import UserCodeService
from cuztomisable.services.users.tokens.access import UserAccessTokenService
from cuztomisable.services.users.tokens.refresh import UserRefreshTokenService
from cuztomisable.settings import settings

router = APIRouter(prefix="/mfa", tags=["MFA"])

_MAX_CODE_ATTEMPTS = settings("multi_factor_authentication.code.max_attempts", 5)
_REMEMBER_FOR = timedelta(days=settings("multi_factor_authentication.remember_for_days", 30))


def _invalid_token() -> CuztomisableException:
    return CuztomisableException(
        code=status.HTTP_400_BAD_REQUEST,
        detail=trans("login.errors.invalid_mfa_token"),
        key="invalid_mfa_token",
        parameters={"redirect": "/login"},
    )


def _wrong_code() -> CuztomisableException:
    return CuztomisableException(
        code=status.HTTP_400_BAD_REQUEST,
        detail=trans("login.errors.mfa_wrong_code"),
        key="mfa_wrong_code",
    )


def _get_valid_record(db: Session, token: str) -> UserCode:
    record = UserCodeService(db).get_by_token(token)
    if not record or record.used_at:
        raise _invalid_token()
    if record.expires_at and record.expires_at < datetime.now(timezone.utc):
        raise _invalid_token()
    return record


@router.get("/{token}/verify", response_model=MfaChannelsResponse)
def verify_token(token: str, db: Session = Depends(get_db)):
    record = _get_valid_record(db, token)
    user = record.user
    email = mask_email(user.email) if user.email else None
    phone = mask_phone(user.phone) if user.phone else None
    if not email and not phone:
        raise CuztomisableException(
            code=status.HTTP_400_BAD_REQUEST,
            detail=trans("login.errors.mfa_no_channels"),
            key="mfa_no_channels",
            parameters={"redirect": "/login"},
        )
    return MfaChannelsResponse(
        message=trans("login.multi_factor_authentication.channels"),
        email=email if settings("login.with.email", True) and email else None,
        phone=phone if settings("login.with.phone", True) and phone else None,
    )


@router.post("/{token}/send", response_model=MessageResponse)
def send_code(token: str, data: MfaSendRequest, db: Session = Depends(get_db)):
    record = _get_valid_record(db, token)
    user = record.user
    resend_timer = settings("multi_factor_authentication.resend_timer", 60)
    if record.sent_at and record.sent_at > datetime.now(timezone.utc) - timedelta(seconds=resend_timer):
        raise CuztomisableException(
            code=status.HTTP_400_BAD_REQUEST,
            detail=trans("login.errors.code_sent_too_recently"),
            key="code_sent_too_recently",
        )
    if settings("multi_factor_authentication.code.regenerate_on_resend", False):
        record.code = UserCodeService(db).generate_code()
    if data.type == "email" and user.email and settings("login.with.email", True):
        UserCodeService(db).send_email(user, record)
    elif data.type == "sms" and user.phone and settings("login.with.phone", True):
        # TODO :: Implement SMS sending logic here
        pass
    record.sent_at = datetime.now(timezone.utc)
    record.sent_via = data.type
    db.commit()
    return MessageResponse(message=trans("login.multi_factor_authentication.sent"))


@router.post("/{token}", response_model=TokenResponse)
def verify_and_login(token: str, data: MfaLoginRequest, db: Session = Depends(get_db)):
    record = UserCodeService(db).get_by_token(token)
    if not record or record.used_at:
        raise _invalid_token()
    if record.code != data.code:
        record.attempt_counter += 1
        if record.attempt_counter >= _MAX_CODE_ATTEMPTS:
            record.used_at = datetime.now(timezone.utc)
            db.commit()
            raise CuztomisableException(
                code=status.HTTP_400_BAD_REQUEST,
                detail=trans("login.errors.mfa_max_attempts_reached"),
                key="mfa_max_attempts_reached",
                parameters={"redirect": "/login"},
            )
        db.commit()
        raise _wrong_code()
    elif record.code == data.code and record.expires_at and record.expires_at < datetime.now(timezone.utc):
        # The code is correct but has expired, so we mark it as used and raise an exception
        record.used_at = datetime.now(timezone.utc)
        db.commit()
        raise CuztomisableException(
            code=status.HTTP_400_BAD_REQUEST,
            detail=trans("login.errors.mfa_code_expired"),
            key="mfa_code_expired",
            parameters={"redirect": "/login"},
        )
    record.used_at = datetime.now(timezone.utc)
    user = record.user
    if data.remember and record.user_ip_address:
        record.user_ip_address.remember = True
        record.user_ip_address.remember_until = datetime.now(timezone.utc) + _REMEMBER_FOR
    access_token, access_record = UserAccessTokenService(db).create(user.id)
    refresh_record = UserRefreshTokenService(db).create(user.id)
    db.commit()
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_record.token,
        expires_at=access_record.expires_at,
        user=UserResponse.model_validate(user).model_dump(mode="json"),
    )
