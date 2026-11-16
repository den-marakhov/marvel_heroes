from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from src.domain.entities.user_session import UserSessionEntity
from src.domain.exceptions import DomainValidationError


def _build_user_session(**overrides) -> UserSessionEntity:
    now = datetime.now(UTC)
    defaults = {
        "session_id": uuid4(),
        "user_id": uuid4(),
        "refresh_jti": str(uuid4()),
        "access_jti": str(uuid4()),
        "ip": "127.0.0.1",
        "user_agent": "Mozilla/5.0",
        "expires_at": now + timedelta(days=30),
        "created_at": now,
        "last_seen_at": now,
    }
    defaults.update(overrides)
    return UserSessionEntity(**defaults)


class TestUserSessionEntity:
    def test_user_session_entity_success(self):
        session_id = uuid4()
        user_id = uuid4()
        refresh_jti = str(uuid4())
        access_jti = str(uuid4())
        now = datetime.now(UTC)
        expires_at = now + timedelta(days=30)

        user_session = _build_user_session(
            session_id=session_id,
            user_id=user_id,
            refresh_jti=refresh_jti,
            access_jti=access_jti,
            created_at=now,
            last_seen_at=now,
            expires_at=expires_at,
        )

        assert user_session.session_id == session_id
        assert user_session.user_id == user_id
        assert user_session.refresh_jti == refresh_jti
        assert user_session.access_jti == access_jti
        assert user_session.ip == "127.0.0.1"
        assert user_session.user_agent == "Mozilla/5.0"
        assert user_session.location is None
        assert user_session.revoked_at is None
        assert user_session.created_at == now
        assert user_session.last_seen_at == now
        assert user_session.expires_at == expires_at

    def test_user_session_entity_with_location_and_revoked_at(self):
        revoked_at = datetime.now(UTC)

        user_session = _build_user_session(
            location="Moscow, Russia",
            revoked_at=revoked_at,
        )

        assert user_session.location == "Moscow, Russia"
        assert user_session.revoked_at == revoked_at

    def test_user_session_entity_empty_refresh_jti(self):
        with pytest.raises(DomainValidationError, match="Refresh jti must not be empty"):
            _build_user_session(refresh_jti="")

    def test_user_session_entity_empty_access_jti(self):
        with pytest.raises(DomainValidationError, match="Access jti must not be empty"):
            _build_user_session(access_jti="")

    def test_user_session_entity_empty_ip(self):
        with pytest.raises(DomainValidationError, match="IP must not be empty"):
            _build_user_session(ip="")

    def test_user_session_entity_empty_user_agent(self):
        with pytest.raises(DomainValidationError, match="User agent must not be empty"):
            _build_user_session(user_agent="")

    def test_user_session_entity_expires_at_not_after_created_at(self):
        now = datetime.now(UTC)

        with pytest.raises(
            DomainValidationError, match="Expiration must be after creation time"
        ):
            _build_user_session(created_at=now, expires_at=now)
