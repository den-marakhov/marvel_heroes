from typing import Any, final
from dataclasses import dataclass

import structlog

from src.application.dtos.hero import HeroDTO
from src.application.interfaces.cache import CacheProtocol
from src.application.interfaces.serialization import SerializationMapperProtocol


logger = structlog.get_logger(__name__)

@final
@dataclass(frozen=True, kw_only=True, slots=True)
class SaveHeroesToCacheUseCase:

	client_cache: CacheProtocol
	serialization_mapper: SerializationMapperProtocol

	async def __call__(self, heroes: list[HeroDTO]) -> None:
		await self.client_cache.set(
			"hero:all",
			{"data": self.serialization_mapper.to_dict_list(heroes)}
		)
		logger.info("Heroes have been saved to cache", heroes_quantity=len(heroes))