from typing import final
from dataclasses import dataclass


from src.application.dtos.hero import(
	HeroDTO,
	ManualCreateHeroDTO,
	HeroNameDTO,
	)



from src.presentation.api.rest.v1.schemes.responses import (
	HeroResponseScheme,
	)

from src.presentation.api.rest.v1.schemes.requests import (
	HeroRequestBodyScheme,
	HeroUpdateRequestScheme
)

@final
@dataclass(frozen=True, slots=True)
class HeroPresentationMapper:

	def to_response_scheme(self, dto: HeroDTO) -> HeroResponseScheme:

		return HeroResponseScheme(
			hero_id=dto.hero_id,
			name=dto.name.value,
			description=dto.description,
			created_at=dto.created_at,
			updated_at=dto.updated_at
		)
	
	def to_manual_hero_create_dto(
			self,
			scheme:HeroRequestBodyScheme
			) -> ManualCreateHeroDTO:
		
		return ManualCreateHeroDTO(
			name=HeroNameDTO(value=scheme.name),
			description=scheme.description
		)

	
