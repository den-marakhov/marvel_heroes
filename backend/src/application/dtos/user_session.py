from dataclasses import dataclass
from datetime import datetime
from typing import final
from uuid import UUID


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class CreateUserSessionDTO:
    session_id: UUID
    user_id: UUID
    access_jti: str
    refresh_jti: str
    ip: str
    user_agent: str
    expires_at: datetime


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class UserSessionDTO:
    session_id: UUID
    user_id: UUID
    ip: str
    user_agent: str
    location: str | None
    created_at: datetime
    last_seen_at: datetime
    expires_at: datetime
