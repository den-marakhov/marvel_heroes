from abc import abstractmethod
from typing import Protocol

from src.application.dtos.hero import(
	HeroDTO,
	ManualCreateHeroDTO,
	UpdateHeroDTO,
	ExternalAPIHeroDTO
)

from src.domain.entities.hero import HeroEntity
from src.domain.value_objects.hero_name import HeroName



class DtoEntityMapperProtocol(Protocol):

	@abstractmethod
	def to_entity_from_manual_hero_create_dto(
		self, dto: ManualCreateHeroDTO
	) -> HeroEntity:
		...
	
	@abstractmethod
	def to_dto(self, entity: HeroEntity) -> HeroDTO:
		...
	
	@abstractmethod
	def to_entity(self, dto: HeroDTO) -> HeroEntity:
		...

	@abstractmethod
	def to_updated_entity(
		self,
		dto: HeroDTO,
		updated_dto: UpdateHeroDTO
	) -> HeroEntity:
		...

	@abstractmethod
	def from_external_dto_to_updated_dto(
		self,
		external_dto: ExternalAPIHeroDTO,
	) -> UpdateHeroDTO:
		...