from dataclasses import dataclass
from typing import final

import structlog

from src.application.dtos.user import UserDTO
from src.application.exceptions.user import UserNotFoundError
from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.interfaces.user.mappers import UserDtoEntityMapperProtocol
from src.application.usecases.users.cache.get_user_by_email_from_cache import (
    GetUserByEmailFromCacheUseCase,
)
from src.application.usecases.users.cache.save_user_to_cache import (
    SaveUserToCacheUseCase,
)
from src.domain.entities.user import UserEntity

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserByEmailFromRepoUseCase:
    uow: UnitOfWorkProtocol
    mapper: UserDtoEntityMapperProtocol
    get_user_by_email_from_cache_usecase: GetUserByEmailFromCacheUseCase
    save_user_to_cache_usecase: SaveUserToCacheUseCase

    async def __call__(self, email: str) -> UserDTO:
        if user_dto := await self.get_user_by_email_from_cache_usecase(email):
            return user_dto

        async with self.uow:
            user_entity: UserEntity | None = await self.uow.users.get_by_email(email)

            if not user_entity:
                raise UserNotFoundError(
                    f"User '{email}' has not been found in database"
                )

            logger.info("User has been found in repository", email=email)
            user_dto = self.mapper.to_dto(user_entity)

        await self.save_user_to_cache_usecase(str(user_entity.user_id), user_dto)

        return user_dto
