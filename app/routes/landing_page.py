from fastapi import APIRouter

from app.controllers import landing_page

router = APIRouter(prefix="/landing_page", tags=["landing_page"])


router.post("/start_consult")(landing_page.start_consult)

router.get("/result/{client_id}")(landing_page.get_result_client_by_id)

router.get("/list-address/{client_id}")(landing_page.get_address)

router.post("/selected_data")(landing_page.selected_data_of_client)
