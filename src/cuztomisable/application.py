import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import CuztomisableConfig
from .db import events  # noqa: F401 — registers SQLAlchemy audit field listeners
from .dependencies import get_session
from .errors import report_error
from .lang import trans
from .middleware.ensure_valid_mobile_agent import EnsureValidMobileAgent
from .middleware.set_locale import SetLocale
from .routers import routers

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
        async def handle_unhandled_exception(request: Request, exc: Exception):
            # Still print the full traceback to the console — a registered
            # handler prevents Starlette's own unhandled-exception logging.
            logger.exception("Unhandled exception during request")

            db = get_session()
            try:
                debug_code = report_error(
                    db,
                    exc,
                    parameters={
                        "path": str(request.url),
                        "method": request.method,
                    },
                )
            finally:
                db.close()

            return JSONResponse(
                status_code=500,
                content={
                    "detail": trans(
                        "global.errors.unexpected",
                        debug_code=debug_code
                    ),
                    "debug_code": debug_code,
                },
            )

        for router in routers:
            app.include_router(router, prefix="/api")