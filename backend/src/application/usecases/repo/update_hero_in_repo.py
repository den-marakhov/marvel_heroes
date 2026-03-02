from typing import final
from dataclasses import dataclass
from uuid import UUID

import structlog

from src.domain.entities.hero import HeroEntity

from src.application.dtos.hero import HeroDTO, UpdateHeroDTO
from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.interfaces.mappers import DtoEntityMapperProtocol

from src.application.usecases.cache.invalidate_hero_cache import InvalidateHeroCacheUseCase
from src.application.usecases.repo.get_hero_by_id_from_repo import GetHeroFromRepoUseCase

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateHeroInRepoUseCase:

	uow: UnitOfWorkProtocol
	mapper: DtoEntityMapperProtocol
	get_hero_from_repo_by_id_usecase: GetHeroFromRepoUseCase
	invalidate_cache_usecase: InvalidateHeroCacheUseCase

	async def __call__(
			self,
			hero_id: UUID,
			dto: UpdateHeroDTO
			) -> HeroDTO:
		
		hero_dto = await self.get_hero_from_repo_by_id_usecase(hero_id=hero_id)
		updated_entity = self.mapper.to_updated_entity(hero_dto, dto)
		

		async with self.uow:
			await self.uow.repository.update_hero(hero_id, updated_entity)	
		
		await self.invalidate_cache_usecase(str(hero_id))
		logger.info(
      "Hero has been updated in repository",
      hero_id=str(hero_id),
    )

		return self.mapper.to_dto(updated_entity)
			

