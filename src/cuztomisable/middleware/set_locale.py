from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from cuztomisable.lang import current_locale
from cuztomisable.settings import settings


class SetLocale(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        accept_language = request.headers.get("Accept-Language", settings.default_language)
        locale = accept_language.split(",")[0].split("-")[0].strip().lower()
        current_locale.set(locale)
        return await call_next(request)
