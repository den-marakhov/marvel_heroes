from dataclasses import dataclass
from typing import final

import structlog

from src.application.dtos.user import CreateUserDTO, UserDTO
from src.application.exceptions.user import UserAlreadyExistsError
from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.interfaces.user.mappers import UserDtoEntityMapperProtocol
from src.application.usecases.users.cache.save_user_to_cache import (
    SaveUserToCacheUseCase,
)
from src.infrastructures.db.exceptions import RepositoryConflictError

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUserInRepoUseCase:
    uow: UnitOfWorkProtocol
    mapper: UserDtoEntityMapperProtocol
    save_user_to_cache_usecase: SaveUserToCacheUseCase

    async def __call__(self, dto: CreateUserDTO) -> UserDTO:
        async with self.uow:
            if await self.uow.users.get_by_email(dto.email):
                raise UserAlreadyExistsError(
                    f"User '{dto.email}' already exists in database"
                )

            user_entity = self.mapper.to_entity_from_create_dto(dto)
            try:
                await self.uow.users.save(user_entity)
            except RepositoryConflictError as e:
                raise UserAlreadyExistsError(
                    f"User '{dto.email}' already exists in database"
                ) from e
            logger.info("User has been saved to database", user_id=user_entity.user_id)
            user_dto = self.mapper.to_dto(user_entity)

        await self.save_user_to_cache_usecase(str(user_entity.user_id), user_dto)
        return user_dto
