import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import random

from .config import CuztomisableConfig
from .exceptions import CuztomisableException
from .helpers.dependencies import get_session
from .helpers.errors import report_error
from .lang import trans
from .middleware.ensure_valid_mobile_agent import EnsureValidMobileAgent
from .middleware.set_locale import SetLocale
from .routers import routers
from .settings import settings

logger = logging.getLogger(__name__)


class Cuztomisable:
    def __init__(
        self,
        app: FastAPI | None = None,
        config: CuztomisableConfig | None = None,
    ):
        self.config = config or CuztomisableConfig()

        if app:
            self.init_app(app)

    def init_app(self, app: FastAPI):
        self.app = app
        app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.cors_origins,
            allow_credentials=self.config.cors_allow_credentials,
            allow_methods=self.config.cors_allow_methods,
            allow_headers=self.config.cors_allow_headers,
        )
        app.add_middleware(EnsureValidMobileAgent)
        app.add_middleware(SetLocale)

        @app.exception_handler(Exception)
        async def handle_exception(request: Request, exc: Exception):
            # Anything that isn't already a CuztomisableException is an
            # unanticipated crash — normalize it into one (500, no key) so
            # the logging/response logic below only has to live in one place.
            if isinstance(exc, CuztomisableException):
                cuztomisable_exception = exc
            else:
                # Still print the full traceback to the console — a registered
                # handler prevents Starlette's own unhandled-exception logging.
                logger.exception("Unhandled exception during request")
                cuztomisable_exception = CuztomisableException(code=500, detail=str(exc), exception=type(exc).__name__)

            debug_code = "".join(random.choices(
                settings.errors["debug_code"]["characters"],
                k=settings.errors["debug_code"].get("length") or 8
            ))
            # Only server errors (>= 500) get written to the error log —
            # routine client errors (bad input, auth, not found) are just
            # noted locally.
            message = (
                trans("global.errors.unexpected", debug_code=debug_code)
                if cuztomisable_exception.status_code >= 500
                else cuztomisable_exception.detail
            )
            db = get_session()
            try:
                debug_code = report_error(
                    db,
                    exc,
                    code=cuztomisable_exception.key,
                    message=cuztomisable_exception.detail,
                    parameters={
                        "path": str(request.url),
                        "method": request.method,
                        **getattr(request.state, "error_parameters", {}),
                        **(cuztomisable_exception.parameters or {}),
                    },
                )
            finally:
                db.close()
            # Prevents issues with leaking server / database errors
            cuztomisable_exception.detail = message
            content = {
                "code": cuztomisable_exception.status_code,
                "detail": cuztomisable_exception.detail,
                "exception": cuztomisable_exception.exception_type,
                "parameters": cuztomisable_exception.parameters,
            }
            if debug_code:
                content["debug_code"] = debug_code

            return JSONResponse(
                status_code=cuztomisable_exception.status_code,
                content=content,
                headers=cuztomisable_exception.headers
            )

        for router in routers:
            app.include_router(router, prefix="/api")