from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from cuztomisable.dependencies import get_db
from cuztomisable.lang import trans
from cuztomisable.schemas.login import RefreshRequest
from cuztomisable.schemas.users.tokens.access import TokenResponse
from cuztomisable.services.users.tokens.access import UserAccessTokenService
from cuztomisable.services.users.tokens.refresh import UserRefreshTokenService

router = APIRouter(tags=["Login"])


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    record = UserRefreshTokenService(db).validate(data.refresh_token)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=trans("global.errors.invalid_or_expired_token"),
        )

    access_token, access_record = UserAccessTokenService(db).create(record.user_id)
    db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=record.token,
        expires_at=access_record.expires_at,
    )
