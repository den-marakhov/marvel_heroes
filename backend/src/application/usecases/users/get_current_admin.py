from dataclasses import dataclass
from typing import final

from src.application.dtos.user import UserDTO
from src.application.exceptions.user import AccessDeniedError
from src.application.usecases.users.get_current_user import GetCurrentUserUseCase
from src.domain.constants import ADMIN_ROLE


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class GetCurrentAdminUseCase:
    get_current_user_usecase: GetCurrentUserUseCase

    async def __call__(self, access_token: str) -> UserDTO:
        user_dto = await self.get_current_user_usecase(access_token)
        if user_dto.role != ADMIN_ROLE:
            raise AccessDeniedError("Admin role required")

        return user_dto
