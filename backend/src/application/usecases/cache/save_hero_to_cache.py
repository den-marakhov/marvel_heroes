from dataclasses import dataclass
from typing import final

import structlog

from src.application.dtos.hero import HeroDTO
from src.application.interfaces.cache import CacheProtocol
from src.application.interfaces.serialization import SerializationMapperProtocol

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class SaveHeroToCacheUseCase:
    cache_client: CacheProtocol
    serialization_mapper: SerializationMapperProtocol

    async def __call__(self, hero_id: str, hero_dto: HeroDTO) -> None:
        await self.cache_client.set(
            f"hero:{hero_id}", self.serialization_mapper.to_dict(hero_dto)
        )
        logger.info("Hero has been saved to cache", hero_id=hero_id)
