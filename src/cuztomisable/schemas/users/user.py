import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from cuztomisable.lang import trans
from cuztomisable.schemas.validators import PhoneMixin, PasswordMixin
from cuztomisable.settings import settings


class UserBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str


class UserCreate(PhoneMixin, PasswordMixin):
    name: str = Field(..., max_length=128)
    username: Optional[str] = Field(None, max_length=128)
    email: EmailStr = Field(..., max_length=128)
    password: str = Field(...)
    timezone: Optional[str] = Field(None, max_length=64)

    @model_validator(mode='after')
    def validate_required_fields(self) -> 'UserCreate':
        if settings.registration["require_username"] and not self.username:
            raise ValueError(trans("validation.errors.username_required"))
        if settings.registration["require_phone"] and not self.phone:
            raise ValueError(trans("validation.errors.phone_required"))
        return self


class UserUpdate(BaseModel):
    pass


class UserResponse(BaseModel):
    pass
