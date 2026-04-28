from dataclasses import dataclass
from typing import final
from uuid import UUID

import structlog

from src.application.dtos.hero import HeroDTO
from src.application.exceptions import HeroNotFoundError
from src.application.interfaces.mappers import DtoEntityMapperProtocol
from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.usecases.cache.get_hero_from_cache import GetHeroFromCacheUseCase
from src.application.usecases.cache.save_hero_to_cache import SaveHeroToCacheUseCase
from src.domain.entities.hero import HeroEntity

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class GetHeroFromRepoUseCase:
    uow: UnitOfWorkProtocol
    mapper: DtoEntityMapperProtocol

    get_hero_from_cache_usecase: GetHeroFromCacheUseCase
    save_hero_to_cache_usecase: SaveHeroToCacheUseCase

    async def __call__(self, hero_id: UUID) -> HeroDTO:

        hero_id_str = str(hero_id)
        if hero_dto := await self.get_hero_from_cache_usecase(hero_id_str):
            return hero_dto

        async with self.uow:
            hero_entity: HeroEntity | None = await self.uow.repository.get_hero_by_id(
                hero_id=hero_id
            )

            if not hero_entity:
                raise HeroNotFoundError(
                    f"Hero '{hero_id}' has not been found in database"
                )

            logger.info("Hero has been found in repository", hero_id=hero_id)
            hero_dto = self.mapper.to_dto(hero_entity)

        await self.save_hero_to_cache_usecase(hero_id_str, hero_dto)

        return hero_dto
