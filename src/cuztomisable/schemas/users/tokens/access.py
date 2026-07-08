import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from cuztomisable.schemas.message import MessageResponse


class TokenResponse(MessageResponse):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime


class UserAccessTokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    user_id: uuid.UUID
    expires_at: Optional[datetime]
    revoked: bool
