from datetime import datetime, timedelta

from fastapi import APIRouter

from app.schemas import DefaultResponse
from app.worker.jobs import check_eligibility

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_checker() -> DefaultResponse:
    """Health checker endpoint"""
    check_eligibility.delay(2)
    return {"status": "success"}
