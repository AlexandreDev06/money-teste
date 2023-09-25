from fastapi import APIRouter

from app.controllers import landing_page

router = APIRouter(prefix="/landing_page" ,tags=["landing_page"])


router.post("/start_consult")(landing_page.start_consult)
