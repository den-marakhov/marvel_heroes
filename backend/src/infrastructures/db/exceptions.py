from typing import final


@final
class RepositoryReadError(Exception):
    """Exception raised when a read operation fails."""


@final
class RepositorySaveError(Exception):
    """Exception raised when a save operation fails."""


@final
class RepositoryConflictError(Exception):
    """Exception raised when a conflict occurs."""
