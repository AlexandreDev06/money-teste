from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_checker():
    """Health checker endpoint"""
    return {"detail": {"status": "ok", "status_code": 0, "version": "0.0.1"}}
