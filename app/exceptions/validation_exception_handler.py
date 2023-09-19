from fastapi.responses import JSONResponse


async def validation_exception_handler(*_):
    """Handle validation exceptions and return a
    JSONResponse with a 400 status code and an error detail.

    Parameters:
        _: Any number of positional arguments.

    Returns:
        JSONResponse: A JSON response with a 400 status code and an error detail.
    """
    return JSONResponse(
        status_code=422,
        content={
            "status": "Error",
            "description": "The format of the JSON sent is incorrect",
        },
    )
