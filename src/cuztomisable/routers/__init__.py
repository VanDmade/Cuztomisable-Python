from .login import router as login_router
from .logout import router as logout_router
from .me import router as me_router
from .refresh import router as refresh_router
from .registration import router as registration_router
from .roles import router as roles_router
from .settings import router as settings_router
from .verification import router as verification_router

routers = [login_router, logout_router, me_router, refresh_router, registration_router, roles_router, settings_router, verification_router]

__all__ = ["login_router", "logout_router", "me_router", "refresh_router", "registration_router", "roles_router", "settings_router", "verification_router", "routers"]
