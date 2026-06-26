from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import CuztomisableConfig


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