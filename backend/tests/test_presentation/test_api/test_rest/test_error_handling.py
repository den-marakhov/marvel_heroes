from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.application.exceptions.user import (
    AUTHENTICATION_REQUIRED_MESSAGE,
    LOGIN_FAILED_MESSAGE,
    AccessDeniedError,
    InvalidCredentialsError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.application.exceptions.user_session import UserSessionNotFoundError
from src.domain.exceptions import (
    InvalidEmailException,
    InvalidPasswordException,
    InvalidRoleException,
    InvalidUserNameException,
)
from src.infrastructures.db.exceptions import (
    RepositoryConflictError,
    RepositoryReadError,
    RepositorySaveError,
)
from src.infrastructures.security.exceptions import TokenStorageError
from src.presentation.api.rest.error_handling import setup_exception_handlers


def _client() -> TestClient:  # noqa: C901
    app = FastAPI()
    setup_exception_handlers(app)

    @app.get("/credentials")
    async def credentials() -> None:
        raise InvalidCredentialsError(LOGIN_FAILED_MESSAGE)

    @app.get("/not-found")
    async def not_found() -> None:
        raise UserNotFoundError("User 'admin@marvel.local' does not exist in database")

    @app.get("/session-not-found")
    async def session_not_found() -> None:
        raise UserSessionNotFoundError(
            "User session '11111111-1111-1111-1111-111111111111' "
            "has not been found in database"
        )

    @app.get("/email")
    async def email() -> None:
        raise InvalidEmailException("Invalid email: nope")

    @app.get("/password")
    async def password() -> None:
        raise InvalidPasswordException("Password must be between 8 and 128 characters")

    @app.get("/role")
    async def role() -> None:
        raise InvalidRoleException("Invalid role: guest")

    @app.get("/user-name")
    async def user_name() -> None:
        raise InvalidUserNameException("User name must be between 2 and 100 characters")

    @app.get("/storage")
    async def storage() -> None:
        raise TokenStorageError("Failed to save token 'auth:refresh:abc'")

    @app.get("/forbidden")
    async def forbidden() -> None:
        raise AccessDeniedError("Admin role required")

    @app.get("/token")
    async def token() -> None:
        raise InvalidTokenError("Invalid token")

    @app.get("/exists")
    async def exists() -> None:
        raise UserAlreadyExistsError(
            "User 'admin@marvel.local' already exists in database"
        )

    @app.get("/repo-conflict")
    async def repo_conflict() -> None:
        raise RepositoryConflictError("Conflict while saving hero 'abc': duplicate")

    @app.get("/repo-read")
    async def repo_read() -> None:
        raise RepositoryReadError("Failed to retrieve user with email: 'admin@x'")

    @app.get("/repo-save")
    async def repo_save() -> None:
        raise RepositorySaveError("Failed to save user 'abc': connection refused")

    return TestClient(app)


def test_invalid_credentials_maps_to_401() -> None:
    response = _client().get("/credentials")

    assert response.status_code == 401
    assert response.json() == {"message": LOGIN_FAILED_MESSAGE}


def test_user_session_not_found_maps_to_404() -> None:
    response = _client().get("/session-not-found")

    assert response.status_code == 404
    assert "has not been found in database" in response.json()["message"]


def test_user_not_found_maps_to_404_without_leaking_email() -> None:
    response = _client().get("/not-found")

    assert response.status_code == 404
    assert response.json() == {"message": "User was not found"}
    assert "admin@marvel.local" not in response.text


def test_invalid_email_maps_to_400() -> None:
    response = _client().get("/email")

    assert response.status_code == 400
    assert response.json() == {"message": "Invalid email: nope"}


def test_invalid_password_maps_to_400() -> None:
    response = _client().get("/password")

    assert response.status_code == 400
    assert "Password must be between 8 and 128 characters" in response.json()["message"]


def test_invalid_role_maps_to_400() -> None:
    response = _client().get("/role")

    assert response.status_code == 400
    assert response.json() == {"message": "Invalid role: guest"}


def test_invalid_user_name_maps_to_400() -> None:
    response = _client().get("/user-name")

    assert response.status_code == 400
    assert "User name must be between 2 and 100 characters" in response.json()["message"]


def test_invalid_token_maps_to_401_without_leaking_jwt() -> None:
    response = _client().get("/token")

    assert response.status_code == 401
    assert response.json() == {"message": AUTHENTICATION_REQUIRED_MESSAGE}
    assert "Invalid token" not in response.text


def test_access_denied_maps_to_403() -> None:
    response = _client().get("/forbidden")

    assert response.status_code == 403
    assert response.json() == {"message": "Forbidden"}


def test_user_already_exists_maps_to_409() -> None:
    response = _client().get("/exists")

    assert response.status_code == 409
    assert response.json() == {
        "message": "User 'admin@marvel.local' already exists in database"
    }


def test_repository_conflict_maps_to_409_without_leaking_details() -> None:
    response = _client().get("/repo-conflict")

    assert response.status_code == 409
    assert response.json() == {"message": "Resource already exists"}
    assert "duplicate" not in response.text
    assert "abc" not in response.text


def test_repository_read_error_maps_to_500_without_leaking_details() -> None:
    response = _client().get("/repo-read")

    assert response.status_code == 500
    assert response.json() == {"message": "Failed to read data"}
    assert "admin@x" not in response.text


def test_repository_save_error_maps_to_500_without_leaking_details() -> None:
    response = _client().get("/repo-save")

    assert response.status_code == 500
    assert response.json() == {"message": "Failed to save data"}
    assert "connection refused" not in response.text


def test_token_storage_error_maps_to_503() -> None:
    response = _client().get("/storage")

    assert response.status_code == 503
    assert response.json() == {"message": "Auth service is unavailable"}
    assert "auth:refresh" not in response.text
