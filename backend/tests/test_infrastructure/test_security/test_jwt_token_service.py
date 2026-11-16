from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
import pytest

from src.application.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from src.application.exceptions.user import InvalidTokenError
from src.infrastructures.security.jwt_token_service import JwtTokenService
from src.infrastructures.security.mappers.jwt_token_mapper import JwtTokenMapper


@pytest.fixture
def token_service() -> JwtTokenService:
    return JwtTokenService(
        secret="test-secret-must-be-at-least-32b",
        access_ttl=900,
        refresh_ttl=2_592_000,
        mapper=JwtTokenMapper(),
    )


def test_create_token_pair(token_service: JwtTokenService) -> None:
    user_id = uuid4()
    session_id = uuid4()

    tokens = token_service.create_token_pair(user_id, session_id)
    access_payload = token_service.decode_token(tokens.access_token)
    refresh_payload = token_service.decode_token(tokens.refresh_token)

    assert tokens.access_payload.user_id == user_id
    assert tokens.refresh_payload.user_id == user_id
    assert tokens.access_payload.session_id == session_id
    assert tokens.refresh_payload.session_id == session_id
    assert tokens.access_payload.token_type == ACCESS_TOKEN_TYPE
    assert tokens.refresh_payload.token_type == REFRESH_TOKEN_TYPE
    assert tokens.access_payload.jti != tokens.refresh_payload.jti
    assert access_payload.jti == tokens.access_payload.jti
    assert refresh_payload.jti == tokens.refresh_payload.jti


def test_decode_invalid_token(token_service: JwtTokenService) -> None:
    with pytest.raises(InvalidTokenError, match="Invalid token"):
        token_service.decode_token("not-a-jwt")


def test_decode_invalid_claims(token_service: JwtTokenService) -> None:
    now = datetime.now(UTC)
    token = jwt.encode(
        {
            "sub": str(uuid4()),
            "jti": str(uuid4()),
            "type": "access",
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(seconds=900)).timestamp()),
        },
        token_service.secret,
        algorithm="HS256",
    )

    with pytest.raises(InvalidTokenError, match="Invalid token"):
        token_service.decode_token(token)
