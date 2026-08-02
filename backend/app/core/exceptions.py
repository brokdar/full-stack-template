"""Application error hierarchy and FastAPI exception handlers.

Services raise :class:`AppError` subclasses; the handlers translate them to
consistent JSON responses so endpoints never need try/except for domain
errors.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base class for domain errors carrying an HTTP status."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class NotFoundError(AppError):
    """The requested resource does not exist."""

    status_code = status.HTTP_404_NOT_FOUND


class ConflictError(AppError):
    """The request conflicts with existing state (e.g. duplicate)."""

    status_code = status.HTTP_409_CONFLICT


class ValidationError(AppError):
    """The request is semantically invalid beyond schema validation."""

    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT


def register_exception_handlers(app: FastAPI) -> None:
    """Attach handlers translating AppError subclasses to JSON responses."""

    @app.exception_handler(AppError)
    async def handle_app_error(_request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
