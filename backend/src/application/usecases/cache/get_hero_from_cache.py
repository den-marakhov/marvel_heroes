from dataclasses import dataclass
from typing import Any, final

import structlog

from src.application.dtos.hero import HeroDTO
from src.application.interfaces.cache import CacheProtocol
from src.application.interfaces.serialization import SerializationMapperProtocol

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class GetHeroFromCacheUseCase:
    cache_client: CacheProtocol
    serialization_mapper: SerializationMapperProtocol

    async def __call__(self, hero_id: str) -> HeroDTO | None:

        cached_hero_data: dict[str, Any] | None = await self.cache_client.get(
            f"hero:{hero_id}"
        )
        if cached_hero_data:
            logger.info("Hero has been found in cache", hero_id=hero_id)
            return self.serialization_mapper.from_dict(cached_hero_data)
        logger.info("Hero hasn't been found in cache", hero_id=hero_id)
        return None
