from fastapi import APIRouter

from app.controllers import clients

router = APIRouter(tags=["clients"], prefix="/clients")

router.get("/pipeline")(clients.get_pipeline_cards)

router.get("/pending_clients")(clients.get_pending_clients)

router.get("/show/{client_id}")(clients.get_client_by_id)

router.get("/{stage}")(clients.get_list_of_clients)

router.post("/send-contract/{client_id}")(clients.send_contract)

router.post("/webhook-contract")(clients.webhook_contract_signed)

router.put("/update-stage")(clients.update_stage)

router.put("/{client_id}")(clients.update_client)