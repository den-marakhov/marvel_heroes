from dataclasses import dataclass
from typing import final

import structlog

from src.application.dtos.hero import HeroDTO, ManualCreateHeroDTO
from src.application.interfaces.mappers import DtoEntityMapperProtocol
from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.usecases.cache.invalidate_hero_cache import (
    InvalidateHeroCacheUseCase,
)

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class ManualHeroCreationInRepoUseCase:
    uow: UnitOfWorkProtocol
    mapper: DtoEntityMapperProtocol
    invalidate_cache_usecase: InvalidateHeroCacheUseCase

    async def __call__(self, hero_dto: ManualCreateHeroDTO) -> HeroDTO:

        async with self.uow:
            hero_entity = self.mapper.to_entity_from_manual_hero_create_dto(hero_dto)

            await self.uow.repository.save_hero(hero_entity)
            logger.info("Hero has been saved to database", hero_id=hero_entity.hero_id)
            dto = self.mapper.to_dto(hero_entity)

        await self.invalidate_cache_usecase()

        return dto
