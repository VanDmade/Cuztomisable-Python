from typing import Literal, Optional

from pydantic import BaseModel

from cuztomisable.schemas.message import MessageResponse


class MfaChannelsResponse(MessageResponse):
    email: Optional[str] = None
    phone: Optional[str] = None


class MfaSendRequest(BaseModel):
    type: Literal["email", "sms"]


class MfaLoginRequest(BaseModel):
    code: str
    remember: Optional[bool] = None
