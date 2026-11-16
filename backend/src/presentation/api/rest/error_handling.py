from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.application.exceptions.hero import (
    HeroNotFoundError,
)
from src.application.exceptions.user import (
    AUTHENTICATION_REQUIRED_MESSAGE,
    AccessDeniedError,
    InvalidCredentialsError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.application.exceptions.user_session import UserSessionNotFoundError
from src.domain.exceptions import DomainError
from src.infrastructures.db.exceptions import (
    RepositoryConflictError,
    RepositoryReadError,
    RepositorySaveError,
)
from src.infrastructures.security.exceptions import TokenStorageError
from src.services.exceptions import ImageProcessingError, ImageValidationError


def _error_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"message": message})


async def handle_hero_not_found(
    _request: Request, exc: HeroNotFoundError
) -> JSONResponse:
    return _error_response(status.HTTP_404_NOT_FOUND, str(exc))


async def handle_user_session_not_found(
    _request: Request, exc: UserSessionNotFoundError
) -> JSONResponse:
    return _error_response(status.HTTP_404_NOT_FOUND, str(exc))


async def handle_invalid_credentials(
    _request: Request, exc: InvalidCredentialsError
) -> JSONResponse:
    return _error_response(status.HTTP_401_UNAUTHORIZED, str(exc))


async def handle_user_not_found(
    _request: Request, _exc: UserNotFoundError
) -> JSONResponse:
    return _error_response(status.HTTP_404_NOT_FOUND, "User was not found")


async def handle_user_already_exists(
    _request: Request, exc: UserAlreadyExistsError
) -> JSONResponse:
    return _error_response(status.HTTP_409_CONFLICT, str(exc))


async def handle_invalid_token(
    _request: Request, _exc: InvalidTokenError
) -> JSONResponse:
    return _error_response(
        status.HTTP_401_UNAUTHORIZED, AUTHENTICATION_REQUIRED_MESSAGE
    )


async def handle_access_denied(
    _request: Request, _exc: AccessDeniedError
) -> JSONResponse:
    return _error_response(status.HTTP_403_FORBIDDEN, "Forbidden")


async def handle_token_storage_error(
    _request: Request, _exc: TokenStorageError
) -> JSONResponse:
    return _error_response(
        status.HTTP_503_SERVICE_UNAVAILABLE, "Auth service is unavailable"
    )


async def handle_domain_error(
    _request: Request, exc: DomainError
) -> JSONResponse:
    return _error_response(status.HTTP_400_BAD_REQUEST, str(exc))


async def handle_image_validation(
    _request: Request, exc: ImageValidationError
) -> JSONResponse:
    return _error_response(status.HTTP_400_BAD_REQUEST, str(exc))


async def handle_image_processing(
    _request: Request, _exc: ImageProcessingError
) -> JSONResponse:
    return _error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to process image"
    )


async def handle_repository_conflict(
    _request: Request, _exc: RepositoryConflictError
) -> JSONResponse:
    return _error_response(status.HTTP_409_CONFLICT, "Resource already exists")


async def handle_repository_read_error(
    _request: Request, _exc: RepositoryReadError
) -> JSONResponse:
    return _error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to read data"
    )


async def handle_repository_save_error(
    _request: Request, _exc: RepositorySaveError
) -> JSONResponse:
    return _error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to save data"
    )


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HeroNotFoundError, handle_hero_not_found)
    app.add_exception_handler(UserSessionNotFoundError, handle_user_session_not_found)
    app.add_exception_handler(InvalidCredentialsError, handle_invalid_credentials)
    app.add_exception_handler(UserNotFoundError, handle_user_not_found)
    app.add_exception_handler(UserAlreadyExistsError, handle_user_already_exists)
    app.add_exception_handler(InvalidTokenError, handle_invalid_token)
    app.add_exception_handler(AccessDeniedError, handle_access_denied)
    app.add_exception_handler(DomainError, handle_domain_error)
    app.add_exception_handler(TokenStorageError, handle_token_storage_error)
    app.add_exception_handler(ImageValidationError, handle_image_validation)
    app.add_exception_handler(ImageProcessingError, handle_image_processing)
    app.add_exception_handler(RepositoryConflictError, handle_repository_conflict)
    app.add_exception_handler(RepositoryReadError, handle_repository_read_error)
    app.add_exception_handler(RepositorySaveError, handle_repository_save_error)
