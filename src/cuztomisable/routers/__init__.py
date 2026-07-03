from .auth import router as auth_router
from .roles import router as roles_router

routers = [auth_router, roles_router]

__all__ = ["auth_router", "roles_router", "routers"]
