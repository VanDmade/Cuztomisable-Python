import secrets
import traceback
from typing import Optional

from sqlalchemy.orm import Session

from cuztomisable.context import current_user_id
from cuztomisable.services.logs.error import ErrorLogService


def report_error(
    db: Session,
    exc: Exception,
    *,
    code: Optional[str] = None,
    message: Optional[str] = None,
    parameters: Optional[dict] = None,
) -> str:
    trace = traceback.extract_tb(exc.__traceback__)
    origin = trace[-1] if trace else None
    debug_code = f"{secrets.randbelow(10**8):08d}"

    ErrorLogService(db).create({
        "user_id": current_user_id.get() if current_user_id.get() is not None else None,
        "message": message or str(exc),
        "file": origin.filename if origin else None,
        "line": origin.lineno if origin else None,
        "code": code or type(exc).__name__[:8],
        "debug_code": debug_code,
        "parameters": parameters,
    })
    db.commit()

    return debug_code
