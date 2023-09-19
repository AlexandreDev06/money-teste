from pydantic import BaseModel


class HTTPValidationError(BaseModel):
    """HTTP validation error"""

    status: str = "Error"
    description: str = "The format of the JSON sent is incorrect"


class DefaultResponse(BaseModel):
    """Default response"""

    status: str = "Success"


# response_model to suegger
response_model = {200: {"model": DefaultResponse}, 422: {"model": HTTPValidationError}}
