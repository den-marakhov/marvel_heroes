from dataclasses import dataclass
from typing import final

import structlog

from src.application.dtos.user import UserDTO
from src.application.interfaces.cache import CacheProtocol
from src.application.interfaces.user.serialization import (
    UserSerializationMapperProtocol,
)

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class SaveUserToCacheUseCase:
    cache_client: CacheProtocol
    serialization_mapper: UserSerializationMapperProtocol

    async def __call__(self, user_id: str, user_dto: UserDTO) -> None:
        cached_user_data = self.serialization_mapper.to_dict(user_dto)
        await self.cache_client.set(f"user:{user_id}", cached_user_data)
        await self.cache_client.set(f"user:email:{user_dto.email}", cached_user_data)
        logger.info("User has been saved to cache", user_id=user_id, email=user_dto.email)
