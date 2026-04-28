from uuid import UUID

from polyfactory.factories import DataclassFactory

from src.application.dtos.hero import (
    HeroDTO,
    HeroNameDTO,
)
from src.domain.entities.hero import HeroEntity
from src.domain.value_objects.hero_name import HeroName
from tests.faker import (
    hero_name,
    text,
    uuid4,
)


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
