from fastapi import APIRouter, Depends

from cuztomisable.db.models.users.user import User
from cuztomisable.dependencies import get_current_user
from cuztomisable.schemas.users.user import UserResponse

router = APIRouter(tags=["Login"])


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user
