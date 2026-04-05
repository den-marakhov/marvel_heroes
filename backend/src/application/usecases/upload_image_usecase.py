from typing import final
from dataclasses import dataclass
from uuid import UUID

import structlog

from src.application.dtos.hero import UpdateHeroDTO

from src.application.usecases.repo.update_hero_in_repo import UpdateHeroInRepoUseCase
from src.application.usecases.repo.get_hero_by_id_from_repo import GetHeroFromRepoUseCase

from src.services.image_service import ImageUploadService

logger = structlog.get_logger(__name__)

@final
@dataclass(frozen=True, kw_only=True, slots=True)
class UploadHeroImageUseCase:
	
	image_service: ImageUploadService
	get_hero_from_repo_usecase: GetHeroFromRepoUseCase
	update_hero_in_repo_usecase: UpdateHeroInRepoUseCase


	async def __call__(self, hero_id: UUID, update_dto: UpdateHeroDTO) -> None:
		
		try:
			hero_dto = await self.get_hero_from_repo_usecase(hero_id=hero_id)
		
			if hero_dto.uploaded_img_url is not None:
				logger.debug("Deleting existing hero image", hero_id=hero_id)
				await self.image_service.delete_image(hero_dto.uploaded_img_url)
		
			await self.update_hero_in_repo_usecase(hero_id=hero_id, dto=update_dto)

		except Exception:
			await self.image_service.delete_image(update_dto.uploaded_img_url)
			raise
