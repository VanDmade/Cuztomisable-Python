from datetime import datetime, timezone
from typing import Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from cuztomisable.dependencies import get_db
from cuztomisable.errors import report_error
from cuztomisable.lang import trans
from cuztomisable.security import hash_password
from cuztomisable.schemas.message import MessageResponse
from cuztomisable.schemas.users.tokens.access import TokenResponse
from cuztomisable.schemas.users.user import UserCreate, UserResponse
from cuztomisable.services.users.registration import UserRegistrationService
from cuztomisable.services.users.verification import UserVerificationService
from cuztomisable.services.users.tokens.access import UserAccessTokenService
from cuztomisable.services.users.tokens.refresh import UserRefreshTokenService
from cuztomisable.services.users.user import UserService
from cuztomisable.services.users.passwords.password import UserPasswordService
from cuztomisable.services.users.ip_address import UserIpAddressService
from cuztomisable.settings import settings

router = APIRouter(tags=["Registration"])


@router.post("/register", response_model=Union[TokenResponse, MessageResponse])
def register(
    data: UserCreate,
    request: Request,
    code: Optional[str] = Query(None, max_length=16),
    db: Session = Depends(get_db),
):
    try:
        user_service = UserService(db)
        # Checks to make sure the email is unique
        if user_service.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=trans("registration.errors.email_already_registered"),
            )
        registration_service = UserRegistrationService(db)
        registration = None
        if code:
            registration = registration_service.get_by_code(code)
            # Prevents having to output this error message multiple times in the code below
            invalid_code = HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=trans("registration.errors.invalid_registration_code"),
            )
            # Code was not found
            if not registration:
                raise invalid_code
            # Code was used and maybe the user already has an account
            if registration.used_at:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=trans("registration.errors.registration_code_already_used")
                )
            # Code expired
            if registration.expires_at and registration.expires_at < datetime.now(timezone.utc):
                raise invalid_code
        else:
            # Checks to see if maybe the user skipped the code
            phone = f"{data.country_code} {data.phone}" if data.phone else None
            registration = registration_service.get_by_email_or_phone(data.email, phone)
            if registration and registration.used_at:
                # Already used the registration, maybe they had their account deleted
                registration = None
        user = user_service.create({
            "name": data.name,
            "username": data.username if data.username else None,
            "email": data.email,
            "password": data.password,
            "timezone": data.timezone,
            "phone": data.phone,
            "country_code": data.country_code,
        })
        # Creates the password entry
        UserPasswordService(db).create(user.id, {"password": hash_password(data.password)})
        # Creates the IP address entry
        UserIpAddressService(db).create(user.id, request)
        if registration:
            registration.user_id = user.id
            registration.used_at = datetime.now(timezone.utc)
        # Flow 1: verification required — account exists, but no tokens until they verify
        if settings.verification["email"] or settings.verification["phone"]:
            verification_service = UserVerificationService(db)
            if settings.verification["email"]:
                verification_service.create(user.id, "email")
            if settings.verification["phone"]:
                verification_service.create(user.id, "phone")
            # Determines what needs to be verified
            if settings.verification["email"] and settings.verification["phone"]:
                verify_via = "email and phone"
            elif settings.verification["email"]:
                verify_via = "email"
            else:
                verify_via = "phone"
            db.commit()
            return MessageResponse(
                message=trans("registration.success_verification_required", type=verify_via),
            )
        # Flow 2: log the user in immediately
        if settings.registration["login_after_registration"]:
            access_token, access_record = UserAccessTokenService(db).create(user.id)
            refresh_record = UserRefreshTokenService(db).create(user.id)
            db.commit()
            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_record.token,
                expires_at=access_record.expires_at,
                message=trans("registration.success_and_logged_in"),
                user=UserResponse.model_validate(user).model_dump(mode="json"),
            )
        # Flow 3: account created, but they need to log in themselves
        db.commit()
        return MessageResponse(
            message=trans("registration.success"),
        )
    except HTTPException: raise
    except Exception as e:
        db.rollback()
        parameters = {
            "email": data.email,
            "username": data.username,
        }
        debug_code = report_error(db, e, parameters=parameters)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=trans("global.errors.unexpected", debug_code=debug_code),
        )
