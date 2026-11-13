from fastapi import APIRouter
from .health_view import router as health_router
from .cat_view import router as cat_router
from .auth_view import router as auth_router
from .math_view import router as math_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(cat_router, tags=["Cat Facts"])
api_router.include_router(auth_router, tags=["Authentication"])
api_router.include_router(math_router, tags=["Math Operations"])

__all__ = ["api_router"]
