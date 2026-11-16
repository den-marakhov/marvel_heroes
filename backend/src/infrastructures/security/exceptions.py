from typing import final


@final
class TokenStorageError(Exception):
    """Raised when token allowlist operation fails."""
