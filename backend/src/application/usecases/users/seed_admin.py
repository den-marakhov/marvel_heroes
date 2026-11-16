from dataclasses import dataclass
from typing import final

import structlog

from src.application.dtos.user import CreateUserDTO
from src.application.exceptions.user import UserAlreadyExistsError
from src.application.usecases.users.repo.create_user_in_repo import (
    CreateUserInRepoUseCase,
)

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class SeedAdminUseCase:
    create_user_in_repo_usecase: CreateUserInRepoUseCase

    async def __call__(self, dto: CreateUserDTO) -> None:
        try:
            user_dto = await self.create_user_in_repo_usecase(dto)
        except UserAlreadyExistsError:
            logger.info("Admin already exists", email=dto.email)
            return

        logger.info("Admin has been seeded", user_id=user_dto.user_id)
