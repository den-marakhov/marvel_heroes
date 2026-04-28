from dataclasses import dataclass
from typing import final

import structlog

from src.application.interfaces.cache import CacheProtocol

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class InvalidateHeroCacheUseCase:
    cache_client: CacheProtocol

    async def __call__(self, hero_id: str | None = None) -> None:
        if hero_id:
            await self.cache_client.delete(f"hero:{hero_id}")
            await self.cache_client.delete("hero:all")
            logger.info(
                "Hero was removed from cache and hero list has been invalidate",
                hero_id=hero_id,
            )
        else:
            deleted_heroes = await self.cache_client.clear("hero:*")
            logger.info("Whole hero cache has been invalidated", deleted=deleted_heroes)
