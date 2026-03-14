from typing import final
from dataclasses import dataclass


from src.application.dtos.hero import(
	HeroDTO,
	ManualCreateHeroDTO,
	HeroNameDTO,
	ExternalAPIHeroDTO
	)



from src.presentation.api.rest.v1.schemes.responses import (
	HeroResponseScheme,
	ExternalHeroResponseScheme
	)

from src.presentation.api.rest.v1.schemes.requests import (
	HeroRequestBodyScheme,
)

@final
@dataclass(frozen=True, slots=True)
class HeroPresentationMapper:

	def to_response_scheme(self, dto: HeroDTO) -> HeroResponseScheme:

		return HeroResponseScheme(
			hero_id=dto.hero_id,
			name=dto.name.value,
			description=dto.description,
			full_name=dto.full_name,
			publisher=dto.publisher,
			external_img_url=dto.external_img_url,
			uploaded_img_url=dto.uploaded_img_url,
			created_at=dto.created_at,
			updated_at=dto.updated_at,
		)
	
	def to_external_api_hero_response_scheme(
			self, dto: ExternalAPIHeroDTO
	) -> ExternalHeroResponseScheme:
		
		return ExternalAPIHeroDTO(
			external_id=dto.external_id,
			name=dto.name,
			full_name=dto.full_name,
			publisher=dto.publisher,
			image_url=dto.image_url
		)
	
	def to_manual_hero_create_dto(
			self,
			scheme:HeroRequestBodyScheme
			) -> ManualCreateHeroDTO:
		
		return ManualCreateHeroDTO(
			name=HeroNameDTO(value=scheme.name),
			description=scheme.description
		)

	
