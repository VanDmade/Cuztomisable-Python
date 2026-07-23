from datetime import datetime

from cuztomisable.schemas.message import MessageResponse
from cuztomisable.schemas.mixins import UserMixin


class TokenResponse(MessageResponse, UserMixin):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime
