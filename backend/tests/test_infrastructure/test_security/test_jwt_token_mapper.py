from datetime import UTC, datetime
from uuid import uuid4

from src.application.dtos.token import AuthTokensDTO, TokenPayload
from src.infrastructures.security.mappers.jwt_token_mapper import JwtTokenMapper


def test_to_token_payload() -> None:
    mapper = JwtTokenMapper()
    user_id = uuid4()
    session_id = uuid4()

    payload = mapper.to_token_payload(
        {
            "sub": str(user_id),
            "sid": str(session_id),
            "jti": "access-jti",
            "type": "access",
            "exp": int(datetime.now(UTC).timestamp()) + 900,
        }
    )

    assert payload.user_id == user_id
    assert payload.session_id == session_id
    assert payload.jti == "access-jti"
    assert payload.token_type == "access"
    assert payload.expires_in <= 900


def test_to_auth_tokens_dto() -> None:
    mapper = JwtTokenMapper()
    user_id = uuid4()
    session_id = uuid4()
    access_payload = TokenPayload(
        user_id=user_id,
        session_id=session_id,
        jti="access-jti",
        token_type="access",
        expires_in=900,
    )
    refresh_payload = TokenPayload(
        user_id=user_id,
        session_id=session_id,
        jti="refresh-jti",
        token_type="refresh",
        expires_in=2_592_000,
    )

    tokens = mapper.to_auth_tokens_dto(
        access_token="access-jwt",
        refresh_token="refresh-jwt",
        access_payload=access_payload,
        refresh_payload=refresh_payload,
    )

    assert tokens.access_token == "access-jwt"
    assert tokens.refresh_token == "refresh-jwt"
    assert tokens.access_payload is access_payload
    assert tokens.refresh_payload is refresh_payload


def test_to_update_session_tokens_dto() -> None:
    mapper = JwtTokenMapper()
    user_id = uuid4()
    session_id = uuid4()
    tokens = AuthTokensDTO(
        access_token="access-jwt",
        refresh_token="refresh-jwt",
        access_payload=TokenPayload(
            user_id=user_id,
            session_id=session_id,
            jti="access-jti",
            token_type="access",
            expires_in=900,
        ),
        refresh_payload=TokenPayload(
            user_id=user_id,
            session_id=session_id,
            jti="refresh-jti",
            token_type="refresh",
            expires_in=2_592_000,
        ),
    )

    dto = mapper.to_update_session_tokens_dto(tokens)

    assert dto.session_id == session_id
    assert dto.user_id == user_id
    assert dto.access_jti == "access-jti"
    assert dto.refresh_jti == "refresh-jti"
    assert dto.access_ttl == 900
    assert dto.refresh_ttl == 2_592_000
