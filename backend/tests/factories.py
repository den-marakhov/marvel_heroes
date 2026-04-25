from polyfactory.factories import DataclassFactory
from uuid import UUID

from tests.faker import (
	uuid4,
	text,
	datetime_current_century,
	hero_name,
	random_int,
	full_name,
	image_url
)

from src.application.dtos.hero import (
	HeroDTO,
	HeroNameDTO,
	ManualCreateHeroDTO,
)

from src.domain.entities.hero import HeroEntity
from src.domain.value_objects.hero_name import HeroName


class HeroNameDTOFactory(DataclassFactory[HeroNameDTO]):
	@classmethod
	def value(cls) -> str:
		return hero_name()
	
	
class HeroNameFactory(DataclassFactory[HeroName]):
	@classmethod
	def value(cls) -> str:
		return hero_name()
	
	
class HeroDTOFactory(DataclassFactory[HeroDTO]):
	@classmethod
	def hero_id(cls) -> UUID:
		return uuid4()
	
	@classmethod
	def name(cls) -> HeroNameDTO:
		return HeroNameDTOFactory.build()
	
	@classmethod
	def description(cls) -> str:
		return text()
	
	
class HeroEntityFactory(DataclassFactory[HeroEntity]):
	@classmethod
	def hero_id(cls) -> UUID:
		return uuid4()

	@classmethod
	def name(cls) -> HeroName:
		return HeroNameFactory.build()
	
	@classmethod
	def description(cls) -> str:
		return text()

