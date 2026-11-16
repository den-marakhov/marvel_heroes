from typing import final


class DomainError(Exception):
    """Base for domain invariant violations."""


@final
class InvalidHeroNameException(DomainError):
    """Raises when invalid name to hero entity is provided"""


@final
class DomainValidationError(DomainError):
    """Raise when entity validation error occurs"""


@final
class InvalidEmailException(DomainError):
    """Raises when invalid email is provided"""


@final
class InvalidUserNameException(DomainError):
    """Raises when invalid user name is provided"""


@final
class InvalidRoleException(DomainError):
    """Raises when invalid role is provided"""


@final
class InvalidPasswordException(DomainError):
    """Raises when invalid raw password is provided"""
