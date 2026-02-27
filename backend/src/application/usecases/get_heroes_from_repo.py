from typing import final
from dataclasses import dataclass

import structlog

from src.application.dtos.hero import HeroDTO
from src.application.interfaces.uow import UnitOfWorkProtocol

from src.application.usecases.get_heroes_from_cache import GetHeroesFromCacheUseCase
from src.application.usecases.save_heroes_to_cache import SaveHeroesToCacheUseCase

from src.application.mappers import DtoEntityMapperProtocol


logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class GetHeroesFromRepoUseCase:
	
	uow: UnitOfWorkProtocol
	mapper: DtoEntityMapperProtocol
	get_heroes_from_cache_usecase: GetHeroesFromCacheUseCase
	save_heroes_to_cache_usecase: SaveHeroesToCacheUseCase

	async def __call__(self) -> list[HeroDTO]:
		if cached_hero_dtos := await self.get_heroes_from_cache_usecase():
			return cached_hero_dtos
		
		async with self.uow:
			hero_entities = await self.uow.repository.get_heroes()
			hero_dtos = [
				self.mapper.to_dto(hero_entity) for hero_entity in hero_entities
			]
			logger.info(
				"Heroes have been retrieved from database",
				heroes_qnty=len(hero_dtos)
				)
		
		await self.save_heroes_to_cache_usecase(heroes=hero_dtos)

		return hero_dtos

