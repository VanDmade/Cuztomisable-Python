from typing import Optional

from pydantic import BaseModel


class UserMixin(BaseModel):
    user: Optional[dict] = None
