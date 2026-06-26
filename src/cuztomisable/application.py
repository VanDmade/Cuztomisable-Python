from fastapi import FastAPI

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
        print("Cuztomisable initialized")