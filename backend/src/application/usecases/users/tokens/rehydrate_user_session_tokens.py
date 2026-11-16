from dataclasses import dataclass
from datetime import UTC, datetime
from typing import final

import structlog

from src.application.constants import ACCESS_TOKEN_TYPE
from src.application.dtos.token import TokenPayload
from src.application.exceptions.user import (
    AUTHENTICATION_REQUIRED_MESSAGE,
    InvalidCredentialsError,
)
from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.interfaces.user.session_token_repository import (
    SessionTokenRepositoryProtocol,
)
from src.application.interfaces.user_session.mappers import (
    UserSessionDtoEntityMapperProtocol,
)
from src.domain.entities.user_session import UserSessionEntity

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class RehydrateUserSessionTokensUseCase:
    uow: UnitOfWorkProtocol
    session_token_repository: SessionTokenRepositoryProtocol
    mapper: UserSessionDtoEntityMapperProtocol

    async def __call__(self, payload: TokenPayload) -> None:
        current_time = datetime.now(UTC)
        async with self.uow:
            user_session_entity: UserSessionEntity | None = (
                await self.uow.user_sessions.get_user_session_by_id(
                    session_id=payload.session_id
                )
            )

        if not user_session_entity:
            raise InvalidCredentialsError(AUTHENTICATION_REQUIRED_MESSAGE)

        stored_token_jti = (
            user_session_entity.access_jti
            if payload.token_type == ACCESS_TOKEN_TYPE
            else user_session_entity.refresh_jti
        )
        if (
            user_session_entity.revoked_at is not None
            or user_session_entity.user_id != payload.user_id
            or user_session_entity.expires_at <= current_time
            or stored_token_jti != payload.jti
        ):
            raise InvalidCredentialsError(AUTHENTICATION_REQUIRED_MESSAGE)

        token_ttl = max(payload.expires_in, 1)
        remaining_session_ttl = max(
            int((user_session_entity.expires_at - current_time).total_seconds()),
            1,
        )
        if payload.token_type == ACCESS_TOKEN_TYPE:
            access_token_ttl = token_ttl
            refresh_token_ttl = remaining_session_ttl
        else:
            access_token_ttl = 1
            refresh_token_ttl = token_ttl

        update_user_session_tokens_dto = self.mapper.to_update_tokens_dto(
            user_session_entity,
            access_ttl=access_token_ttl,
            refresh_ttl=refresh_token_ttl,
        )
        await self.session_token_repository.update_session_tokens(
            update_user_session_tokens_dto
        )
        logger.info(
            "User session tokens have been rehydrated",
            session_id=payload.session_id,
            user_id=payload.user_id,
        )
