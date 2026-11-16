from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import final
from uuid import UUID

from src.domain.exceptions import DomainValidationError


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class UserSessionEntity:
    session_id: UUID
    user_id: UUID
    refresh_jti: str
    access_jti: str
    ip: str
    user_agent: str
    expires_at: datetime
    location: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    last_seen_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    revoked_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.refresh_jti:
            raise DomainValidationError("Refresh jti must not be empty")

        if not self.access_jti:
            raise DomainValidationError("Access jti must not be empty")

        if not self.ip:
            raise DomainValidationError("IP must not be empty")

        if not self.user_agent:
            raise DomainValidationError("User agent must not be empty")

        if self.expires_at <= self.created_at:
            raise DomainValidationError("Expiration must be after creation time")
