from dataclasses import dataclass
from typing import final
from uuid import UUID

import structlog

from src.application.dtos.user import UserDTO
from src.application.exceptions.user import UserNotFoundError
from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.interfaces.user.mappers import UserDtoEntityMapperProtocol
from src.application.usecases.users.cache.get_user_from_cache import (
    GetUserFromCacheUseCase,
)
from src.application.usecases.users.cache.save_user_to_cache import (
    SaveUserToCacheUseCase,
)
from src.domain.entities.user import UserEntity

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserFromRepoUseCase:
    uow: UnitOfWorkProtocol
    mapper: UserDtoEntityMapperProtocol
    get_user_from_cache_usecase: GetUserFromCacheUseCase
    save_user_to_cache_usecase: SaveUserToCacheUseCase

    async def __call__(self, user_id: UUID) -> UserDTO:
        user_id_str = str(user_id)
        if user_dto := await self.get_user_from_cache_usecase(user_id_str):
            return user_dto

        async with self.uow:
            user_entity: UserEntity | None = await self.uow.users.get_by_id(user_id)

            if not user_entity:
                raise UserNotFoundError(
                    f"User '{user_id}' has not been found in database"
                )

            logger.info("User has been found in repository", user_id=user_id)
            user_dto = self.mapper.to_dto(user_entity)

        await self.save_user_to_cache_usecase(user_id_str, user_dto)

        return user_dto
