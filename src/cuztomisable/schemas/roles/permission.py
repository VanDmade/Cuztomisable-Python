import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RolePermissionCreate(BaseModel):
    permission_id: uuid.UUID


class RolePermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    role_id: uuid.UUID
    permission_id: uuid.UUID
