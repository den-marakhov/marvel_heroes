from dataclasses import dataclass
from typing import final

import structlog

from src.application.dtos.token import AuthTokensDTO
from src.application.dtos.user_session import CreateUserSessionDTO
from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.interfaces.user.session_token_repository import (
    SessionTokenRepositoryProtocol,
)
from src.application.interfaces.user_session.mappers import (
    UserSessionDtoEntityMapperProtocol,
)

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class SaveUserSessionToRepoUseCase:
    uow: UnitOfWorkProtocol
    session_token_repository: SessionTokenRepositoryProtocol
    mapper: UserSessionDtoEntityMapperProtocol

    async def __call__(
        self, dto: CreateUserSessionDTO, tokens: AuthTokensDTO
    ) -> None:
        async with self.uow:
            user_session_entity = self.mapper.to_entity_from_create_dto(dto)
            await self.uow.user_sessions.save_user_session(user_session_entity)
            await self.session_token_repository.save_token_pair(tokens)
            logger.info(
                "User session has been saved to repo",
                user_id=dto.user_id,
                session_id=dto.session_id,
            )
