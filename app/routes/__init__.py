from fastapi import APIRouter

from .health import router as router_health

routers = APIRouter(prefix="/api/v1")

routers.include_router(router_health)
