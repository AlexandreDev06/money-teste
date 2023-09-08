from fastapi import APIRouter

from app.controllers import operations

router = APIRouter(tags=["operations"], prefix="/operations")


router.post("/uploads")(operations.create_new_operation)
