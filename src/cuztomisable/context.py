import uuid
from contextvars import ContextVar
from typing import Optional

current_user_id: ContextVar[Optional[uuid.UUID]] = ContextVar("current_user_id", default=None)
