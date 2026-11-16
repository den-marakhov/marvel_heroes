from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from src.application.dtos.token import AuthTokensDTO, TokenPayload
from src.application.dtos.user_session import UserSessionDTO
from src.presentation.api.rest.v1.mappers.user_mapper import UserPresentationMapper
from src.presentation.api.rest.v1.schemes.users.requests import LoginRequestScheme


@pytest.fixture
def mapper() -> UserPresentationMapper:
    return UserPresentationMapper()


def test_to_login_dto(mapper: UserPresentationMapper) -> None:
    scheme = LoginRequestScheme(email="admin@marvel.local", password="secretpassword")

    dto = mapper.to_login_dto(scheme, ip="127.0.0.1", user_agent="Mozilla/5.0")

    assert dto.email == scheme.email
    assert dto.password == scheme.password
    assert dto.ip == "127.0.0.1"
    assert dto.user_agent == "Mozilla/5.0"


def test_to_auth_response_exposes_only_access_token(
    mapper: UserPresentationMapper,
) -> None:
    user_id = uuid4()
    session_id = uuid4()
    dto = AuthTokensDTO(
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

    response = mapper.to_auth_response(dto)

    assert response.access_token == "access-jwt"
    assert response.token_type == "bearer"
    assert "refresh_token" not in response.model_dump()


def test_to_session_response_scheme(mapper: UserPresentationMapper) -> None:
    now = datetime.now(UTC)
    dto = UserSessionDTO(
        session_id=uuid4(),
        user_id=uuid4(),
        ip="127.0.0.1",
        user_agent="Mozilla/5.0",
        location="Moscow, Russia",
        created_at=now,
        last_seen_at=now,
        expires_at=now + timedelta(days=30),
    )

    response = mapper.to_session_response_scheme(dto)

    assert response.session_id == dto.session_id
    assert response.user_id == dto.user_id
    assert response.ip == dto.ip
    assert response.user_agent == dto.user_agent
    assert response.location == dto.location
    assert response.created_at == dto.created_at
    assert response.last_seen_at == dto.last_seen_at
    assert response.expires_at == dto.expires_at
    assert "refresh_jti" not in response.model_dump()
    assert "access_jti" not in response.model_dump()


def test_to_session_response_scheme_list(mapper: UserPresentationMapper) -> None:
    now = datetime.now(UTC)
    dtos = [
        UserSessionDTO(
            session_id=uuid4(),
            user_id=uuid4(),
            ip="127.0.0.1",
            user_agent="Mozilla/5.0",
            location=None,
            created_at=now,
            last_seen_at=now,
            expires_at=now + timedelta(days=30),
        ),
        UserSessionDTO(
            session_id=uuid4(),
            user_id=uuid4(),
            ip="10.0.0.1",
            user_agent="curl/8.0",
            location=None,
            created_at=now,
            last_seen_at=now,
            expires_at=now + timedelta(days=30),
        ),
    ]

    responses = mapper.to_session_response_scheme_list(dtos)

    assert [response.session_id for response in responses] == [
        dto.session_id for dto in dtos
    ]
    assert mapper.to_session_response_scheme_list([]) == []
