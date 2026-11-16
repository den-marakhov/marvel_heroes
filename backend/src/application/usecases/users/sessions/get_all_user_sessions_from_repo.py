from dataclasses import dataclass
from typing import final

import structlog

from src.application.dtos.user_session import UserSessionDTO
from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.interfaces.user_session.mappers import (
    UserSessionDtoEntityMapperProtocol,
)

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class GetAllUserSessionsFromRepoUseCase:
    uow: UnitOfWorkProtocol
    mapper: UserSessionDtoEntityMapperProtocol

    async def __call__(self) -> list[UserSessionDTO]:
        async with self.uow:
            user_session_entities = (
                await self.uow.user_sessions.get_all_user_sessions()
            )
            user_session_dtos = self.mapper.to_dto_list(user_session_entities)
            logger.info(
                "User sessions have been retrieved from database",
                user_sessions_qnty=len(user_session_dtos),
            )

        return user_session_dtos
