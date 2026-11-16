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
class DeleteAllUserSessionTokensUseCase:
    session_token_repository: SessionTokenRepositoryProtocol

    async def __call__(self, user_id: UUID) -> None:
        await self.session_token_repository.delete_all(user_id)
        logger.info("User session tokens have been deleted", user_id=user_id)
