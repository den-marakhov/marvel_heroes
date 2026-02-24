from dataclasses import dataclass
from typing import final
from uuid import UUID

import structlog

from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.interfaces.mappers import DtoEntityMapperProtocol

from src.domain.entities.hero import HeroEntity
from src.application.exceptions import HeroNotFoundError

logger = structlog.getLogger(__name__)

@final
@dataclass(frozen=True, kw_only=True, slots=True)
class DeleteHeroFromRepoUseCase:

		uow: UnitOfWorkProtocol

		async def __call__(
			self,
			hero_id: UUID
		) -> None:

			async with self.uow:
				hero_entity: (
					HeroEntity | None
				) = await self.uow.repository.get_hero_by_id(hero_id=hero_id)

				if not hero_entity:
					raise HeroNotFoundError(
						f"Hero '{hero_id}' does not exist in database"
					)
				
				await self.uow.repository.delete_hero(hero_id)
				logger.info("Hero has been deleted from repo", hero_id=hero_id)

