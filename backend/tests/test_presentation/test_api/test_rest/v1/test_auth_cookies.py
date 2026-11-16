from unittest.mock import MagicMock

from fastapi import Response

from src.presentation.api.rest.v1.auth_cookies import (
    REFRESH_COOKIE_NAME,
    REFRESH_COOKIE_PATH,
    clear_refresh_cookie,
    set_refresh_cookie,
)


def test_set_refresh_cookie_http_only_and_path() -> None:
    response = Response()
    settings = MagicMock()
    settings.environment = "local"
    settings.jwt_refresh_ttl = 2_592_000

    set_refresh_cookie(response, "refresh-jwt", settings)

    cookie = response.headers.get("set-cookie")
    assert cookie is not None
    assert f"{REFRESH_COOKIE_NAME}=refresh-jwt" in cookie
    assert "HttpOnly" in cookie
    assert f"Path={REFRESH_COOKIE_PATH}" in cookie
    assert "Secure" not in cookie


def test_set_refresh_cookie_secure_in_prod() -> None:
    response = Response()
    settings = MagicMock()
    settings.environment = "prod"
    settings.jwt_refresh_ttl = 2_592_000

    set_refresh_cookie(response, "refresh-jwt", settings)

    cookie = response.headers.get("set-cookie")
    assert cookie is not None
    assert "Secure" in cookie


def test_clear_refresh_cookie() -> None:
    response = Response()
    settings = MagicMock()
    settings.environment = "local"

    clear_refresh_cookie(response, settings)

    cookie = response.headers.get("set-cookie")
    assert cookie is not None
    assert f"{REFRESH_COOKIE_NAME}=" in cookie
    assert "Max-Age=0" in cookie
    assert f"Path={REFRESH_COOKIE_PATH}" in cookie
