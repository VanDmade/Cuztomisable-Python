from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from cuztomisable.dependencies import get_db
from cuztomisable.lang import trans
from cuztomisable.schemas.users.tokens.access import TokenResponse
from cuztomisable.schemas.users.user import UserCreate
from cuztomisable.services.phones import PhoneService
from cuztomisable.services.users.registration import UserRegistrationService
from cuztomisable.services.users.tokens.access import UserAccessTokenService
from cuztomisable.services.users.tokens.refresh import UserRefreshTokenService
from cuztomisable.services.users.user import UserService

router = APIRouter(tags=["Registration"])


@router.post("/register", response_model=TokenResponse)
def register(
    data: UserCreate,
    code: Optional[str] = Query(None, max_length=16),
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    if user_service.get_by_email(data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=trans("registration.errors.email_already_registered"),
        )

    registration_service = UserRegistrationService(db)
    registration = None
    if code:
        registration = registration_service.get_by_code(code)
        invalid_code = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=trans("registration.errors.invalid_registration_code"),
        )
        if not registration or registration.used_at:
            raise invalid_code
        if registration.expires_at and registration.expires_at < datetime.now(timezone.utc):
            raise invalid_code
        if registration.email and registration.email.lower() != data.email.lower():
            registration.attempt_counter += 1
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=trans("registration.errors.registration_email_mismatch"),
            )

    user = user_service.create({
        "name": data.name,
        "username": data.username,
        "email": data.email,
        "password": data.password,
        "timezone": data.timezone,
    })

    if data.phone:
        PhoneService(db).create(user.id, {
            "number": data.phone,
            "country_code": str(data.country_code) if data.country_code else None,
        })

    if registration:
        registration.user_id = user.id
        registration.used_at = datetime.now(timezone.utc)
        db.commit()

    access_token, access_record = UserAccessTokenService(db).create(user.id)
    refresh_record = UserRefreshTokenService(db).create(user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_record.token,
        expires_at=access_record.expires_at,
    )
