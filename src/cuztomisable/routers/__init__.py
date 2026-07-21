from .auth.login import router as login_router
from .auth.logout import router as logout_router
from .auth.me import router as me_router
from .auth.mfa import router as mfa_router
from .auth.password import router as password_router
from .auth.refresh import router as refresh_router
from .auth.registration import router as registration_router
from .auth.verification import router as verification_router
from .roles import router as roles_router
from .settings import router as settings_router

routers = [
    login_router,
    logout_router,
    me_router,
    mfa_router,
    password_router,
    refresh_router,
    registration_router,
    verification_router,
    roles_router,
    settings_router,
]

__all__ = [
    "login_router",
    "logout_router",
    "me_router",
    "mfa_router",
    "password_router",
    "refresh_router",
    "registration_router",
    "verification_router",
    "roles_router",
    "settings_router",
    "routers",
]
