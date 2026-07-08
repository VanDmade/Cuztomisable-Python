from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from cuztomisable.dependencies import get_db
from cuztomisable.lang import trans
from cuztomisable.schemas.message import MessageResponse
from cuztomisable.services.users.user import UserService

router = APIRouter(tags=["Registration"])


@router.get("/{token}/v/{value}", response_model=MessageResponse)
def verify(token: str, value: str, db: Session = Depends(get_db)):
    user = UserService(db).get_by_token(token)
    if user:
        # Determines if value is an email or phone and the user needs to be verified
        if (user.email_verified_at is None and "@" in value) or \
            (user.phone_verified_at is None and "@" not in value):
            if "@" in value:
                user.email_verified_at = datetime.now(timezone.utc)
            else:
                user.phone_verified_at = datetime.now(timezone.utc)
        db.commit()
    # To prevent any issues with the user clicking the link multiple times
    # or someone else trying to use the same token, we will always return
    # a success message even if the user is not found or already verified.
    return MessageResponse(message=trans("registration.verification_success"))
