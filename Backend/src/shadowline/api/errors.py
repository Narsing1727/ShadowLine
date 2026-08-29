"""Custom error types and exception handlers."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class ShadowLineException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ResourceNotFoundError(ShadowLineException):
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(f"{resource_type} with id '{resource_id}' not found.", status_code=404)


class InvalidModeTransitionError(ShadowLineException):
    def __init__(self, reason: str):
        super().__init__(f"Cannot transition mode: {reason}", status_code=422)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ShadowLineException)
    async def shadowline_exception_handler(request: Request, exc: ShadowLineException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.__class__.__name__, "message": exc.message},
        )
