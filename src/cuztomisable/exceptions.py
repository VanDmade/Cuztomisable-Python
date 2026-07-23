from typing import Optional


class CuztomisableException(Exception):
    """
    Raised for any expected, request-invalidating error (bad input, auth
    failure, missing resource, etc). Caught by the handler registered in
    application.py, which logs it (only when code >= 500) and returns a
    uniform JSON body — callers don't need to catch it themselves.
    """

    def __init__(
        self,
        code: int,
        message: str,
        key: Optional[str] = None,
        parameters: Optional[dict] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        self.status_code = code
        self.message = message
        self.key = key
        self.parameters = parameters
        self.headers = headers
        super().__init__(message)

