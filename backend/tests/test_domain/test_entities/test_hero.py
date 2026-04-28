from datetime import datetime
from uuid import uuid4

import pytest

from src.domain.entities.hero import HeroEntity
from src.domain.exceptions import DomainValidationError, InvalidHeroNameException
from src.domain.value_objects.hero_name import HeroName


class TestHeroEntity:
    def test_hero_entity_success(self):
        """Test successful creation of HeroEntity"""

        hero_id = uuid4()

        hero_entity = HeroEntity(
            hero_id=hero_id,
            name=HeroName(value="Spider-Man"),
            description="Great power comes with great responsibility",
        )

        assert hero_entity.hero_id == hero_id
        assert hero_entity.name.value == "Spider-Man"
        assert hero_entity.description == "Great power comes with great responsibility"
        assert isinstance(hero_entity.created_at, datetime)
        assert isinstance(hero_entity.updated_at, datetime)
        assert hero_entity.external_id is None
        assert hero_entity.publisher is None
        assert hero_entity.full_name is None
        assert hero_entity.uploaded_img_url is None

    def test_hero_entity_invalid_hero_name(self):
        """Test unsuccessful creation of HeroEntity with invalid name"""

        with pytest.raises(InvalidHeroNameException):
            HeroEntity(
                hero_id=uuid4(),
                name=HeroName(value="Batman"),
                description="description",
            )

    def test_hero_entity_invalid_description(self):
        """
        Test unsuccessful creation of HeroEntity with invalid description length
        """

        with pytest.raises(DomainValidationError):
            HeroEntity(
                hero_id=uuid4(),
                name=HeroName(value="Spider-Man"),
                description="v" * 1001,
            )

    def test_hero_entity_invalid_full_name_too_short(self):
        with pytest.raises(InvalidHeroNameException):
            HeroEntity(
                hero_id=uuid4(),
                name=HeroName(value="Spider-Man"),
                description="Great power comes with great responsibility",
                full_name="P",
            )

    def test_hero_entity_invalid_full_name_too_long(self):
        with pytest.raises(InvalidHeroNameException):
            HeroEntity(
                hero_id=uuid4(),
                name=HeroName(value="Spider-Man"),
                description="Great power comes with great responsibility",
                full_name="P" * 201,
            )
