from fastapi import APIRouter

from app.controllers import operations

router = APIRouter(tags=["operations"], prefix="/operations")

router.get("/")(operations.get_list_of_operations)

router.post("/uploads")(operations.create_new_operation)

router.post("/play_pause/{operation_id}")(operations.play_pause)
