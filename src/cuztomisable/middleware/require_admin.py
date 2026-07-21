from fastapi import Depends, status

from cuztomisable.db.models.users.user import User
from cuztomisable.exceptions import CuztomisableException
from cuztomisable.helpers.dependencies import get_current_user
from cuztomisable.lang import trans


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.admin:
        raise CuztomisableException(
            code=status.HTTP_403_FORBIDDEN,
            detail=trans("global.errors.unauthorized"),
            key="forbidden",
        )
    return current_user
