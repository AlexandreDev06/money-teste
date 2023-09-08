from pydantic import BaseModel


class DefaultResponse(BaseModel):
    """Default response"""

    status: str
