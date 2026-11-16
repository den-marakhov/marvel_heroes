from dataclasses import dataclass
from typing import Any, final

import structlog

from src.application.dtos.user import UserDTO
from src.application.interfaces.cache import CacheProtocol
from src.application.interfaces.user.serialization import (
    UserSerializationMapperProtocol,
)

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class GetUserFromCacheUseCase:
    cache_client: CacheProtocol
    serialization_mapper: UserSerializationMapperProtocol

    async def __call__(self, user_id: str) -> UserDTO | None:
        cached_user_data: dict[str, Any] | None = await self.cache_client.get(
            f"user:{user_id}"
        )
        if cached_user_data:
            logger.info("User has been found in cache", user_id=user_id)
            return self.serialization_mapper.from_dict(cached_user_data)
        logger.info("User hasn't been found in cache", user_id=user_id)
        return None
