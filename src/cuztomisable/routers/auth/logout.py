from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from cuztomisable.db.models.users.user import User
from cuztomisable.helpers.dependencies import get_current_user, get_db
from cuztomisable.schemas.authentication import LogoutRequest
from cuztomisable.services.users.tokens.refresh import UserRefreshTokenService

router = APIRouter(tags=["Login"])


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    data: LogoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    refresh_service = UserRefreshTokenService(db)
    record = refresh_service.get_by_token(data.refresh_token)
    if record and record.user_id == current_user.id:
        refresh_service.revoke(record.id)
