from typing import final
from dataclasses import dataclass
from uuid import uuid4

from src.application.interfaces.mappers import DtoEntityMapperProtocol

from src.domain.entities.hero import HeroEntity
from src.domain.value_objects.hero_name import HeroName
from src.application.dtos.hero import (
	HeroDTO,
	HeroNameDTO,
	ManualCreateHeroDTO
	)

@final
@dataclass(frozen=True, slots=True)
class HeroMapper(DtoEntityMapperProtocol):
	
	def to_entity_from_manual_hero_create_dto(
			self, dto: ManualCreateHeroDTO
	) -> HeroEntity:
		
		return HeroEntity(
			hero_id=uuid4(),
			name=HeroName(value=dto.name.value),
			description=dto.description
		)
	
	def to_dto(self, entity: HeroEntity) -> HeroDTO:

		return HeroDTO(
			hero_id=entity.hero_id,
			name=HeroNameDTO(value=entity.name.value),
			description=entity.description,
			created_at=entity.created_at,
			updated_at=entity.updated_at
		)
	
	def to_entity(self, dto: HeroDTO) -> HeroEntity:
		
		return HeroEntity(
			hero_id=dto.hero_id,
			name=HeroName(value=dto.name.value),
			description=dto.description,
			created_at=dto.created_at,
			updated_at=dto.updated_at
		)
