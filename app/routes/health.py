from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_checker():
    """Health checker endpoint"""
    return {"status": "success"}
