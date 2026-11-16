from dataclasses import dataclass
from typing import Literal, final
from uuid import UUID

TokenType = Literal["access", "refresh"]


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class TokenPayload:
    user_id: UUID
    session_id: UUID
    jti: str
    token_type: TokenType
    expires_in: int


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class AuthTokensDTO:
    access_token: str
    refresh_token: str
    access_payload: TokenPayload
    refresh_payload: TokenPayload


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateUserSessionTokensDTO:
    session_id: UUID
    user_id: UUID
    access_jti: str
    refresh_jti: str
    access_ttl: int
    refresh_ttl: int
