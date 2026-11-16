from dataclasses import dataclass
from typing import final
from uuid import UUID

import structlog

from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.usecases.users.tokens.delete_all_user_session_tokens import (
    DeleteAllUserSessionTokensUseCase,
)

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class RevokeAllUserSessionsFromRepoUseCase:
    uow: UnitOfWorkProtocol
    delete_all_user_session_tokens_usecase: DeleteAllUserSessionTokensUseCase

    async def __call__(self, user_id: UUID) -> None:
        async with self.uow:
            await self.uow.user_sessions.revoke_all_user_sessions(user_id)
            await self.delete_all_user_session_tokens_usecase(user_id)
            logger.info("User sessions have been revoked from repo", user_id=user_id)
