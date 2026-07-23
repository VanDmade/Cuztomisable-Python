from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, TypeAdapter, model_validator

from cuztomisable.helpers.identify import detect_login_type
from cuztomisable.settings import settings


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
        username, login_type = detect_login_type(
            str(data.get("username", "")),
            allow_email=settings.login["with"]["email"],
            allow_phone=settings.login["with"]["phone"],
        )
        data["username"] = username
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
