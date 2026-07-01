import logging
import re

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from cuztomisable.lang import trans
from cuztomisable.settings import settings

logger = logging.getLogger(__name__)


def _parse_version(v: str) -> tuple:
    return tuple(int(x) for x in v.split("."))


class EnsureValidMobileAgent(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_agent = request.headers.get("User-Agent", "")
        is_mobile = request.headers.get("X-App-Platform") == "mobile"

        if not is_mobile or not settings.mobile_agent_enabled:
            return await call_next(request)

        platform_pattern = "|".join(re.escape(p) for p in settings.mobile_agent_platforms)

        for app in settings.mobile_agent_apps:
            app_name = app.get("name", "") if isinstance(app, dict) else str(app)
            if not app_name:
                continue

            pattern = rf"{re.escape(app_name)}/v([0-9]+\.[0-9]+(?:\.[0-9]+)?) \(({platform_pattern})\)"
            match = re.search(pattern, user_agent)

            if match:
                detected_version = match.group(1)
                min_version = app.get("min_version") if isinstance(app, dict) else None

                if min_version and detected_version:
                    if _parse_version(detected_version) < _parse_version(min_version):
                        return JSONResponse(
                            status_code=426,
                            content={
                                "message": trans("global.errors.upgrade"),
                                "upgrade_required": True,
                                "min_version": min_version,
                            },
                        )

                return await call_next(request)

        if settings.mobile_agent_apps:
            if settings.mobile_agent_log_invalid:
                logger.warning(
                    "Invalid mobile user agent",
                    extra={"user_agent": user_agent, "apps": settings.mobile_agent_apps},
                )

            return JSONResponse(
                status_code=403,
                content={
                    "message": trans("global.errors.invalid_user_agent"),
                    "upgrade_required": False,
                },
            )

        return await call_next(request)
