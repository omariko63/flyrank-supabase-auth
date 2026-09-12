from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    error = exc.errors()[0]

    field = error["loc"][-1]
    message = error["msg"]

    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "field": field,
                "message": message,
            }
        },
    )