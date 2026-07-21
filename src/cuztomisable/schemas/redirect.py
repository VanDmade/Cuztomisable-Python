from typing import Optional

from cuztomisable.schemas.message import MessageResponse
from cuztomisable.schemas.mixins import UserMixin


class RedirectMessageResponse(MessageResponse, UserMixin):
    url: str
    data: Optional[dict] = None
