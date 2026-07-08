from typing import Optional

from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: Optional[str] = None
    user: Optional[dict] = None
