from dataclasses import dataclass
from typing import final
from uuid import UUID

import structlog

from src.application.exceptions.user_session import UserSessionNotFoundError
from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.usecases.users.tokens.delete_user_session_tokens import (
    DeleteUserSessionTokensUseCase,
)
from src.domain.entities.user_session import UserSessionEntity

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class RevokeUserSessionFromRepoUseCase:
    uow: UnitOfWorkProtocol
    delete_user_session_tokens_usecase: DeleteUserSessionTokensUseCase

    async def __call__(
        self, user_id: UUID | None, session_id: UUID
    ) -> None:
        async with self.uow:
            user_session_entity: UserSessionEntity | None = (
                await self.uow.user_sessions.get_user_session_by_id(
                    session_id=session_id
                )
            )
            if (
                not user_session_entity
                or user_session_entity.revoked_at is not None
                or (
                    user_id is not None
                    and user_session_entity.user_id != user_id
                )
            ):
                raise UserSessionNotFoundError(
                    f"User session '{session_id}' has not been found in database"
                )

            session_owner_id = user_session_entity.user_id
            await self.uow.user_sessions.revoke_session(session_id)
            await self.delete_user_session_tokens_usecase(
                session_id=session_id, user_id=session_owner_id
            )
            logger.info(
                "User session has been revoked from repo",
                user_id=session_owner_id,
                session_id=session_id,
            )
