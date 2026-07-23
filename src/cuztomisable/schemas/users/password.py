from typing import Literal

from cuztomisable.helpers.identify import detect_login_type
from cuztomisable.schemas.message import MessageResponse
from pydantic import BaseModel, Field, model_validator

from cuztomisable.schemas.validators import PasswordMixin
from cuztomisable.settings import settings


class IdentifyResetMixin(BaseModel):
    username: str
    type: Literal["email", "phone"] = "email"

    @model_validator(mode="before")
    @classmethod
    def prepare(cls, data):
        if not isinstance(data, dict):
            return data
        data = dict(data)
        username, type = detect_login_type(
            str(data.get("username", "")),
            allow_email=settings("reset_password.with.email", True),
            allow_phone=settings("reset_password.with.phone", False),
        )
        data["username"] = username
        data["type"] = type
        return data


class ForgotPasswordRequest(IdentifyResetMixin):
    pass


class ForgotPasswordResponse(MessageResponse):
    username: str
    pass


class VerifyResetCodeQuery(IdentifyResetMixin):
    pass


class ForgotPasswordSendRequest(IdentifyResetMixin):
    pass


class ResetPasswordRequest(PasswordMixin, IdentifyResetMixin):
    password: str = Field(...)
    code: str = Field(
        ...,
        min_length=settings("reset_password.code.length", 6),
        max_length=settings("reset_password.code.length", 6)
    )
