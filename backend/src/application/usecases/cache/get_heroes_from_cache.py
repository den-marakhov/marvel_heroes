from typing import Any, final
from dataclasses import dataclass

import structlog

from src.application.dtos.hero import HeroDTO

from src.application.interfaces.cache import CacheProtocol
from src.application.interfaces.serialization import SerializationMapperProtocol

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class GetHeroesFromCacheUseCase:

	cache_client: CacheProtocol
	serialization_mapper: SerializationMapperProtocol

	async def __call__(self) ->list[HeroDTO] | None:
		cached_data: (
			list[dict[str, Any]] | None
		) = await self.cache_client.get("hero:all")

		if cached_data:
			return self.serialization_mapper.from_dict_list(cached_data["data"])
		
		logger.info("Heroes list hasn't been found in cache")
		return None