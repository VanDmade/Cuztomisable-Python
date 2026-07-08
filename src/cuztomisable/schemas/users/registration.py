from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserRegistrationCreate(BaseModel):
    name: Optional[str] = Field(None, max_length=128)
    email: Optional[EmailStr] = Field(None, max_length=128)
    phone: Optional[str] = Field(None, max_length=15)


class UserRegistrationUpdate(BaseModel):
    pass


class UserRegistrationResponse(BaseModel):
    pass
