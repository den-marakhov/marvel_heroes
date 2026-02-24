from dataclasses import dataclass
from typing import final

from uuid import UUID

import structlog

from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.interfaces.mappers import DtoEntityMapperProtocol

from src.domain.entities.hero import HeroEntity
from src.application.dtos.hero import HeroDTO

from src.application.exceptions import HeroNotFoundError

logger = structlog.get_logger(__name__)

@final
@dataclass(frozen=True, kw_only=True, slots=True)
class GetHeroFromRepoUseCase:

	uow: UnitOfWorkProtocol
	mapper: DtoEntityMapperProtocol

	async def __call__(
			self,
			hero_id: UUID
			) -> HeroDTO:
		
		async with self.uow:
			hero_entity: (
				HeroEntity | None
			) = await self.uow.repository.get_hero_by_id(hero_id=hero_id)

			if not hero_entity:
				raise HeroNotFoundError(
					f"Hero '{hero_id}' has not been found in database"
				)

			logger.info("Hero has been found in repository", hero_id=hero_id)
			return self.mapper.to_dto(hero_entity)
		
			

	