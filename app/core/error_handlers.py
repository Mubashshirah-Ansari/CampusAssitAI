
import logging

from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI):

    # Handle HTTP errors such as 401, 404 and 429
    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException
    ):
        request_id = getattr(request.state, "request_id", "unknown")

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "type": "HTTP_ERROR",
                    "message": str(exc.detail),
                    "request_id": request_id
                }
            },
            headers=exc.headers
        )

    # Handle invalid request data
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):
        request_id = getattr(request.state, "request_id", "unknown")

        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "type": "VALIDATION_ERROR",
                    "message": "Invalid request data. Please check your input.",
                    "request_id": request_id
                }
            }
        )

    # Handle unexpected application errors
    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request,
        exc: Exception
    ):
        request_id = getattr(request.state, "request_id", "unknown")

        logger.exception(
            "Unexpected error | Request ID: %s",
            request_id
        )

        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "type": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected server error occurred.",
                    "request_id": request_id
                }
            }
        )
