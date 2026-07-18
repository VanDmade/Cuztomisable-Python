from typing import Optional

from pydantic import BaseModel, Field

from cuztomisable.schemas.validators import PasswordMixin


class ForgotPasswordRequest(BaseModel):
    username: str
    type: Optional[str] = None


class ForgotPasswordResponse(BaseModel):
    message: str
    # Dev-only stand-in until real email/SMS delivery exists — see the note
    # in routers/password.py. Never ship this field once delivery is wired up.
    token: Optional[str] = None


class ResetPasswordRequest(PasswordMixin):
    code: str
    password: str = Field(...)
