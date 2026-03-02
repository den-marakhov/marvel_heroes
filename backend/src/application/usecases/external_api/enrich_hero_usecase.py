from typing import final
from dataclasses import dataclass
from uuid import UUID

import structlog

from src.application.dtos.hero import HeroDTO
from src.application.interfaces.http_clients import ExternalMarvelApiProtocol
from src.application.mappers import DtoEntityMapperProtocol

from src.application.usecases.repo.update_hero_in_repo import UpdateHeroInRepoUseCase


logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class EnrichHeroUseCase:

	marvel_hero_api_client: ExternalMarvelApiProtocol
	mapper: DtoEntityMapperProtocol
	update_hero_in_repo_usecase: UpdateHeroInRepoUseCase

	async def __call__(
			self,
			hero_id: UUID,
			external_id: int
	) -> HeroDTO:
		
		external_hero_dto = (
			await self.marvel_hero_api_client
			.fetch_hero_by_external_id(external_id=external_id)
		)
		hero_update_dto = (
			self.mapper.from_external_dto_to_updated_dto(external_hero_dto)
		)

		hero_dto = await self.update_hero_in_repo_usecase(
			hero_id=hero_id, dto=hero_update_dto
		)
		logger.info(
			"Hero enriched successfully",
			hero_id=str(hero_id),
			external_id=external_id
		)

		return hero_dto



