from typing import Final, final

LOGIN_FAILED_MESSAGE: Final = "Invalid email or password"
AUTHENTICATION_REQUIRED_MESSAGE: Final = "Authentication required"


@final
class UserNotFoundError(Exception):
    """Raises when a user is not found"""


@final
class UserAlreadyExistsError(Exception):
    """Raises when a user with this email already exists"""


@final
class InvalidCredentialsError(Exception):
    """Raises when login fails or the current session is invalid"""


@final
class InvalidTokenError(Exception):
    """Raises when a JWT cannot be decoded or required claims are missing"""


@final
class AccessDeniedError(Exception):
    """Raises when the current user is not allowed to perform the action"""
