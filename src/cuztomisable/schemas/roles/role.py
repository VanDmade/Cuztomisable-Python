import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from cuztomisable.schemas.users.user import UserBrief


class RoleCreate(BaseModel):
    name: str = Field(..., max_length=128)
    slug: str = Field(..., max_length=64)
    description: Optional[str] = None


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=128)
    slug: Optional[str] = Field(None, max_length=64)
    description: Optional[str] = None


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    created_by_user: Optional[UserBrief] = None
    updated_at: datetime
    deleted_at: Optional[datetime]
    deleted_by_user: Optional[UserBrief] = None
    name: str
    slug: str
    description: Optional[str]
