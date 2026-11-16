from typing import final


@final
class UserSessionNotFoundError(Exception):
    """Raises when a user session is not found or does not belong to the user"""
