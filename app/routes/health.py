from fastapi import APIRouter

from app.schemas import DefaultResponse

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_checker() -> DefaultResponse:
    """Health checker endpoint"""
    return {"status": "Success"}
