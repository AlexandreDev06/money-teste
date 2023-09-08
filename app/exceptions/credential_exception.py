from fastapi.responses import JSONResponse


class CredentialsException(Exception):
    """A class that handles the case when the credentials are invalid."""

    message = "Invalid Bearer Token"

    def __init__(self, message=message) -> None:
        self.message = message


async def credentials_invalid_exception(_, exc):
    """Generates the exception response for invalid credentials.

    Parameters:
        _: Placeholder parameter. Ignored.
        exc (Exception): The exception object.

    Returns:
        JSONResponse: The JSON response with the error details.
    """
    return JSONResponse(
        status_code=401,
        content={"status": "Error", "description": exc.message},
        headers={"WWW-Authenticate": "Bearer"},
    )
