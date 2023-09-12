from fastapi import APIRouter

from app.controllers import clients

router = APIRouter(tags=["clients"], prefix="/clients")

router.put("/update-stage")(clients.update_stage)

router.get("/{stage}")(clients.get_list_of_clients)
