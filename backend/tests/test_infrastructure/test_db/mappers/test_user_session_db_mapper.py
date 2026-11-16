from datetime import UTC, datetime, timedelta
from uuid import uuid4

from src.domain.entities.user_session import UserSessionEntity
from src.infrastructures.db.mappers.user_session_db_mapper import UserSessionDBMapper


def _user_session_entity(**overrides) -> UserSessionEntity:
    now = datetime.now(UTC)
    defaults = {
        "session_id": uuid4(),
        "user_id": uuid4(),
        "refresh_jti": str(uuid4()),
        "access_jti": str(uuid4()),
        "ip": "127.0.0.1",
        "user_agent": "Mozilla/5.0",
        "location": "Moscow, Russia",
        "expires_at": now + timedelta(days=30),
        "created_at": now,
        "last_seen_at": now,
        "revoked_at": None,
    }
    defaults.update(overrides)
    return UserSessionEntity(**defaults)


def test_user_session_db_mapper_roundtrip() -> None:
    mapper = UserSessionDBMapper()
    entity = _user_session_entity()

    model = mapper.to_model(entity)
    restored = mapper.to_entity(model)

    assert restored.session_id == entity.session_id
    assert restored.user_id == entity.user_id
    assert restored.refresh_jti == entity.refresh_jti
    assert restored.access_jti == entity.access_jti
    assert restored.ip == entity.ip
    assert restored.user_agent == entity.user_agent
    assert restored.location == entity.location
    assert restored.expires_at == entity.expires_at
    assert restored.created_at == entity.created_at
    assert restored.last_seen_at == entity.last_seen_at
    assert restored.revoked_at is None


def test_user_session_db_mapper_update_model_from_entity() -> None:
    mapper = UserSessionDBMapper()
    entity = _user_session_entity()
    model = mapper.to_model(entity)

    revoked_at = datetime.now(UTC)
    updated = _user_session_entity(
        session_id=entity.session_id,
        user_id=entity.user_id,
        refresh_jti=str(uuid4()),
        access_jti=str(uuid4()),
        ip="10.0.0.1",
        user_agent="Chrome",
        location=None,
        created_at=entity.created_at,
        last_seen_at=revoked_at,
        expires_at=entity.expires_at,
        revoked_at=revoked_at,
    )

    mapper.update_model_from_entity(model, updated)

    assert model.refresh_jti == updated.refresh_jti
    assert model.access_jti == updated.access_jti
    assert model.ip == "10.0.0.1"
    assert model.user_agent == "Chrome"
    assert model.location is None
    assert model.last_seen_at == revoked_at
    assert model.revoked_at == revoked_at
    assert model.session_id == entity.session_id
    assert model.user_id == entity.user_id
