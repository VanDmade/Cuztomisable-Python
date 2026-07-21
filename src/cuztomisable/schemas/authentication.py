from typing import Literal, Optional

from cuztomisable.schemas.message import MessageResponse
from pydantic import BaseModel, EmailStr, TypeAdapter, model_validator

from cuztomisable.settings import settings

_PHONE_STRIP_CHARS = ("/", "_", "-", "(", ")", " ")


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class MfaChannelsResponse(MessageResponse):
    email: Optional[str] = None
    phone: Optional[str] = None


class MfaSendRequest(BaseModel):
    type: Literal["email", "sms"]


class MfaLoginRequest(BaseModel):
    code: str
    remember: Optional[bool] = None


class LoginRequest(BaseModel):
    username: str
    password: str
    type: Literal["email", "phone", "username"] = "username"
    remember: Optional[bool] = None
    timezone: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def prepare(cls, data):
        if not isinstance(data, dict):
            return data
        data = dict(data)
        raw_username = str(data.get("username", "")).strip()

        wants_phone = settings.login["with"]["phone"] and "@" not in raw_username
        login_type = "phone" if wants_phone else ("email" if settings.login["with"]["email"] else "username")

        if login_type == "phone":
            for char in _PHONE_STRIP_CHARS:
                raw_username = raw_username.replace(char, "")
            # Falls back to email if the cleaned value isn't actually a phone number
            if not raw_username.isdigit():
                login_type = "email"
        elif login_type == "email":
            raw_username = raw_username.lower()

        data["username"] = raw_username
        data["type"] = login_type
        return data

    @model_validator(mode="after")
    def validate_rules(self) -> "LoginRequest":
        if not self.username:
            raise ValueError("username is required")
        if not self.password:
            raise ValueError("password is required")
        if self.type == "email":
            TypeAdapter(EmailStr).validate_python(self.username)
        if self.remember is None:
            self.remember = False
        return self
