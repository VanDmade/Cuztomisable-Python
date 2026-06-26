import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ImageCreate(BaseModel):
    url: str
    filename: str
    content_type: str
    size: int


class ImageResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    url: str
    filename: str
    content_type: str
    size: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
