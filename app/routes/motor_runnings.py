from fastapi import APIRouter

from app.controllers import motor_runnings

router = APIRouter(tags=["motor_runnings"], prefix="/motor_runnings")


router.post("/play_pause/{id}")(motor_runnings.play_pause)
