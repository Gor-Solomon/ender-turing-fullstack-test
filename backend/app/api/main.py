from fastapi import APIRouter

from app.api.routes import items, login, metrics, private, users, utils
from app.core.config import settings

api_router = APIRouter()

# Register routers
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(items.router, tags=["items"])
api_router.include_router(metrics.router, tags=["metrics"])
api_router.include_router(utils.router, tags=["utils"])

if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router, prefix="/private", tags=["private"])