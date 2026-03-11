from .health import router as health_router
from .documents import router as documents_router
from .auth import router as auth_router

__all__ = ["health_router", "documents_router", "auth_router"]
