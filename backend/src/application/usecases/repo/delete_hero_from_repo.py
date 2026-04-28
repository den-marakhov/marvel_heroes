from dataclasses import dataclass
from typing import final
from uuid import UUID

import structlog

from src.application.exceptions import HeroNotFoundError
from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.usecases.cache.invalidate_hero_cache import (
    InvalidateHeroCacheUseCase,
)
from src.domain.entities.hero import HeroEntity

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class DeleteHeroFromRepoUseCase:
    uow: UnitOfWorkProtocol
    invalidate_cache_usecase: InvalidateHeroCacheUseCase

    async def __call__(self, hero_id: UUID) -> None:

        async with self.uow:
            hero_entity: HeroEntity | None = await self.uow.repository.get_hero_by_id(
                hero_id=hero_id
            )

            if not hero_entity:
                raise HeroNotFoundError(f"Hero '{hero_id}' does not exist in database")

            await self.uow.repository.delete_hero(hero_id)
            logger.info("Hero has been deleted from repo", hero_id=hero_id)

        await self.invalidate_cache_usecase(hero_id=str(hero_id))
