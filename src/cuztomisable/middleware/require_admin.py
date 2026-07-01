from fastapi import Depends, HTTPException, status

from cuztomisable.db.models.users.user import User
from cuztomisable.dependencies import get_current_user
from cuztomisable.lang import trans


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=trans("global.errors.unauthorized"))
    return current_user
