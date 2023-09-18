from fastapi import APIRouter

from app.controllers import clients

router = APIRouter(tags=["clients"], prefix="/clients")

router.put("/update-stage")(clients.update_stage)

router.get("/pipeline")(clients.get_pipeline_cards)

router.get("/{stage}")(clients.get_list_of_clients)

router.get("/show/{client_id}")(clients.get_client_by_id)
