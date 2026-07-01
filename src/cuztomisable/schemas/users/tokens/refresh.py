import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserRefreshTokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    user_id: uuid.UUID
    expires_at: Optional[datetime]
    revoked: bool
