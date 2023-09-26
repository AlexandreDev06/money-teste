from fastapi import APIRouter

from .clients import router as router_clients
from .health import router as router_health
from .landing_page import router as router_landing_page
from .motor_runnings import router as router_motor_runnings
from .operations import router as router_operations

routers = APIRouter(prefix="/api/v1")

routers.include_router(router_motor_runnings)
routers.include_router(router_operations)
routers.include_router(router_clients)
routers.include_router(router_landing_page)
routers.include_router(router_health)
