from fastapi.responses import JSONResponse


class ValueNotFound(Exception):
    """A class that handles the case when a value is not found."""

    message = "Value not found"

    def __init__(self, message=message) -> None:
        self.message = message


async def value_not_found(_, exe):
    """A function that handles the case when a value is not found.

    Parameters:
        _: An unused parameter.
        exe (Exception): The exception that was raised when the value was not found.

    Returns:
        JSONResponse: The response object with a status code of 404 and a content
        dictionary containing details about the error.
    """
    return JSONResponse(
        status_code=404, content={"status": "Error", "description": exe.message}
    )
