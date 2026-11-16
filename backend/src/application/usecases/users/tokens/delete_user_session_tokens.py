from dataclasses import dataclass
from typing import final
from uuid import UUID

import structlog

from src.application.interfaces.user.session_token_repository import (
    SessionTokenRepositoryProtocol,
)

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class DeleteUserSessionTokensUseCase:
    session_token_repository: SessionTokenRepositoryProtocol

    async def __call__(self, session_id: UUID, user_id: UUID) -> None:
        await self.session_token_repository.delete_tokens(session_id, user_id)
        logger.info(
            "User session tokens have been deleted",
            session_id=session_id,
            user_id=user_id,
        )
