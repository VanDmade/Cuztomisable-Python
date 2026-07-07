from .login import router as login_router
from .registration import router as registration_router
from .roles import router as roles_router
from .settings import router as settings_router

routers = [login_router, registration_router, roles_router, settings_router]

__all__ = ["login_router", "registration_router", "roles_router", "settings_router", "routers"]
