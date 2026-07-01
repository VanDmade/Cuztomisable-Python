import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class UserBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str


class UserCreate(BaseModel):
    name: str = Field(..., max_length=128)
    username: Optional[str] = Field(None, max_length=128)
    email: EmailStr = Field(..., max_length=128)
    password: str = Field(..., min_length=8, max_length=64)
    password_confirmation: str
    timezone: Optional[str] = Field(None, max_length=64)

    @model_validator(mode='after')
    def passwords_match(self) -> 'UserCreate':
        if self.password != self.password_confirmation:
            raise ValueError('Passwords do not match')
        return self


class UserUpdate(BaseModel):
    pass


class UserResponse(BaseModel):
    pass
