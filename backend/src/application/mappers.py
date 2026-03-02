from typing import final
from dataclasses import dataclass
from uuid import uuid4

from src.application.interfaces.mappers import DtoEntityMapperProtocol

from src.domain.entities.hero import HeroEntity
from src.domain.value_objects.hero_name import HeroName
from src.application.dtos.hero import (
	HeroDTO,
	HeroNameDTO,
	ManualCreateHeroDTO,
	UpdateHeroDTO,
	ExternalAPIHeroDTO
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
			updated_at=entity.updated_at,
			external_id=entity.external_id,
			full_name=entity.full_name,
			publisher=entity.publisher,
			external_img_url=entity.external_img_url,
			uploaded_img_url=entity.uploaded_img_url
		)
	
	def to_entity(self, dto: HeroDTO) -> HeroEntity:
		
		return HeroEntity(
			hero_id=dto.hero_id,
			name=HeroName(value=dto.name.value),
			description=dto.description,
			created_at=dto.created_at,
			updated_at=dto.updated_at,
			external_id=dto.external_id,
			full_name=dto.full_name,
			publisher=dto.publisher,
			external_img_url=dto.external_img_url,
			uploaded_img_url=dto.uploaded_img_url
		)
	
	def to_updated_entity(
			self,
			dto: HeroDTO,
			updated_dto: UpdateHeroDTO
	) -> HeroEntity:
		return HeroEntity(
			hero_id=dto.hero_id,
			name=(
				HeroName(value=updated_dto.name.value)
				if updated_dto.name is not None
				else HeroName(value=dto.name.value)
			),
			description=(
				updated_dto.description
				if updated_dto.description is not None
				else dto.description
			),
			created_at=dto.created_at,
			external_id=(
				updated_dto.external_id
				if updated_dto.external_id is not None
				else dto.external_id
			),
			full_name=(
				updated_dto.full_name
				if updated_dto.full_name is not None
				else dto.full_name
			),
			publisher=(
				updated_dto.publisher
				if updated_dto.publisher is not None
				else dto.publisher
			),
			external_img_url=(
				updated_dto.external_img_url
        if updated_dto.external_img_url is not None
        else dto.external_img_url
			),
			uploaded_img_url=(
				updated_dto.uploaded_img_url
        if updated_dto.uploaded_img_url is not None
        else dto.uploaded_img_url
			)
		)
	
	def from_external_dto_to_updated_dto(
			self,
			external_dto: ExternalAPIHeroDTO,
	) -> UpdateHeroDTO:
		return UpdateHeroDTO(
			external_id=external_dto.external_id,
			full_name=external_dto.full_name,
			publisher=external_dto.publisher,
			external_img_url=external_dto.image_url
		)
	
	
