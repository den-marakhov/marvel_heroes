from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, final
from uuid import UUID

from src.application.dtos.token import (
    AuthTokensDTO,
    TokenPayload,
    UpdateUserSessionTokensDTO,
)


@final
@dataclass(frozen=True, slots=True)
class JwtTokenMapper:
    def to_token_payload(self, token_data: dict[str, Any]) -> TokenPayload:
        return TokenPayload(
            user_id=UUID(str(token_data["sub"])),
            session_id=UUID(str(token_data["sid"])),
            jti=str(token_data["jti"]),
            token_type=token_data["type"],
            expires_in=max(
                int(token_data["exp"]) - int(datetime.now(UTC).timestamp()),
                0,
            ),
        )

    def to_auth_tokens_dto(
        self,
        *,
        access_token: str,
        refresh_token: str,
        access_payload: TokenPayload,
        refresh_payload: TokenPayload,
    ) -> AuthTokensDTO:
        return AuthTokensDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            access_payload=access_payload,
            refresh_payload=refresh_payload,
        )

    def to_update_session_tokens_dto(
        self, tokens: AuthTokensDTO
    ) -> UpdateUserSessionTokensDTO:
        return UpdateUserSessionTokensDTO(
            session_id=tokens.access_payload.session_id,
            user_id=tokens.access_payload.user_id,
            access_jti=tokens.access_payload.jti,
            refresh_jti=tokens.refresh_payload.jti,
            access_ttl=tokens.access_payload.expires_in,
            refresh_ttl=tokens.refresh_payload.expires_in,
        )
