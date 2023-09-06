from fastapi.responses import JSONResponse


class CredentialsException(Exception):
    message = "Invalid Bearer Token"

    def __init__(self, message=message) -> None:
        self.message = message


async def credentials_invalid_exception(_, exc):
    return JSONResponse(
        status_code=401,
        content={
            "detail": {
                "status": "Error",
                "status_code": 3,
                "description": exc.message,
            }
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
