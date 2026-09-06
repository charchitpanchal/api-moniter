import logging
from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("exceptions.handlers")


def _error_response(status_code: int, error: str, message: str, path: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": status_code,
            "error": error,
            "message": message,
            "path": path,
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Centralized exception handling. Ensures:
    - Consistent JSON error shape across the whole API
    - No internal stack traces or file paths ever leak to the client
    - Unexpected errors are logged server-side for debugging
    """

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return _error_response(
            status_code=exc.status_code,
            error=exc.__class__.__name__,
            message=str(exc.detail),
            path=str(request.url.path),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return _error_response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error="VALIDATION_ERROR",
            message="Request validation failed.",
            path=str(request.url.path),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
        return _error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred. Please try again later.",
            path=str(request.url.path),
        )