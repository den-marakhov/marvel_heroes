from datetime import UTC, datetime, timedelta
from uuid import uuid4

from src.application.dtos.token import TokenPayload
from src.application.dtos.user import LoginDTO
from src.application.dtos.user_session import CreateUserSessionDTO
from src.application.mappers.user_session import UserSessionDtoEntityMapper
from src.domain.entities.user_session import UserSessionEntity


def test_to_create_dto() -> None:
    mapper = UserSessionDtoEntityMapper()
    session_id = uuid4()
    user_id = uuid4()
    login_dto = LoginDTO(
        email="admin@marvel.local",
        password="secretpassword",
        ip="127.0.0.1",
        user_agent="Mozilla/5.0",
    )
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

    before = datetime.now(UTC)
    dto = mapper.to_create_dto(
        login_dto,
        session_id=session_id,
        user_id=user_id,
        access_payload=access_payload,
        refresh_payload=refresh_payload,
    )
    after = datetime.now(UTC)

    assert dto.session_id == session_id
    assert dto.user_id == user_id
    assert dto.access_jti == "access-jti"
    assert dto.refresh_jti == "refresh-jti"
    assert dto.ip == "127.0.0.1"
    assert dto.user_agent == "Mozilla/5.0"
    assert (
        before + timedelta(seconds=2_592_000)
        <= dto.expires_at
        <= after + timedelta(seconds=2_592_000)
    )


def test_to_entity_from_create_dto() -> None:
    mapper = UserSessionDtoEntityMapper()
    now = datetime.now(UTC)
    dto = CreateUserSessionDTO(
        session_id=uuid4(),
        user_id=uuid4(),
        access_jti="access-jti",
        refresh_jti="refresh-jti",
        ip="127.0.0.1",
        user_agent="Mozilla/5.0",
        expires_at=now + timedelta(days=30),
    )

    entity = mapper.to_entity_from_create_dto(dto)

    assert entity.session_id == dto.session_id
    assert entity.user_id == dto.user_id
    assert entity.access_jti == dto.access_jti
    assert entity.refresh_jti == dto.refresh_jti
    assert entity.ip == dto.ip
    assert entity.user_agent == dto.user_agent
    assert entity.expires_at == dto.expires_at
    assert entity.revoked_at is None


def test_to_dto() -> None:
    mapper = UserSessionDtoEntityMapper()
    now = datetime.now(UTC)
    entity = UserSessionEntity(
        session_id=uuid4(),
        user_id=uuid4(),
        refresh_jti="refresh-jti",
        access_jti="access-jti",
        ip="127.0.0.1",
        user_agent="Mozilla/5.0",
        location="Moscow, Russia",
        expires_at=now + timedelta(days=30),
        created_at=now,
        last_seen_at=now,
    )

    dto = mapper.to_dto(entity)

    assert dto.session_id == entity.session_id
    assert dto.user_id == entity.user_id
    assert dto.ip == entity.ip
    assert dto.user_agent == entity.user_agent
    assert dto.location == entity.location
    assert dto.created_at == entity.created_at
    assert dto.last_seen_at == entity.last_seen_at
    assert dto.expires_at == entity.expires_at
    assert not hasattr(dto, "refresh_jti")
    assert not hasattr(dto, "access_jti")


def test_to_dto_list() -> None:
    mapper = UserSessionDtoEntityMapper()
    now = datetime.now(UTC)
    entities = [
        UserSessionEntity(
            session_id=uuid4(),
            user_id=uuid4(),
            refresh_jti="refresh-jti",
            access_jti="access-jti",
            ip="127.0.0.1",
            user_agent="Mozilla/5.0",
            expires_at=now + timedelta(days=30),
            created_at=now,
            last_seen_at=now,
        ),
        UserSessionEntity(
            session_id=uuid4(),
            user_id=uuid4(),
            refresh_jti="refresh-jti-2",
            access_jti="access-jti-2",
            ip="10.0.0.1",
            user_agent="curl/8.0",
            expires_at=now + timedelta(days=30),
            created_at=now,
            last_seen_at=now,
        ),
    ]

    dtos = mapper.to_dto_list(entities)

    assert [dto.session_id for dto in dtos] == [
        entity.session_id for entity in entities
    ]
    assert mapper.to_dto_list([]) == []


def test_to_update_tokens_dto() -> None:
    mapper = UserSessionDtoEntityMapper()
    now = datetime.now(UTC)
    entity = UserSessionEntity(
        session_id=uuid4(),
        user_id=uuid4(),
        refresh_jti="refresh-jti",
        access_jti="access-jti",
        ip="127.0.0.1",
        user_agent="Mozilla/5.0",
        expires_at=now + timedelta(days=30),
        created_at=now,
        last_seen_at=now,
    )

    dto = mapper.to_update_tokens_dto(
        entity, access_ttl=400, refresh_ttl=2_592_000
    )

    assert dto.session_id == entity.session_id
    assert dto.user_id == entity.user_id
    assert dto.access_jti == entity.access_jti
    assert dto.refresh_jti == entity.refresh_jti
    assert dto.access_ttl == 400
    assert dto.refresh_ttl == 2_592_000
