from typing import Final

from fastapi import Response

from src.config.base import Settings

REFRESH_COOKIE_NAME: Final = "refresh_token"
REFRESH_COOKIE_PATH: Final = "/api/v1/users"


def set_refresh_cookie(
    response: Response,
    refresh_token: str,
    settings: Settings,
) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.environment == "prod",
        samesite="lax",
        max_age=settings.jwt_refresh_ttl,
        path=REFRESH_COOKIE_PATH,
    )


def clear_refresh_cookie(response: Response, settings: Settings) -> None:
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path=REFRESH_COOKIE_PATH,
        httponly=True,
        secure=settings.environment == "prod",
        samesite="lax",
    )
