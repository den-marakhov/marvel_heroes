import pytest

from src.domain.constants import ALLOWED_NAMES
from src.domain.exceptions import InvalidHeroNameException
from src.domain.value_objects.hero_name import HeroName


class TestHeroName:
    def test_hero_name_successful_creation(self):
        for name in ALLOWED_NAMES:
            hero_name = HeroName(value=name)
            assert hero_name.value == name

    def test_hero_name_unsuccessful_creation(self):
        with pytest.raises(InvalidHeroNameException):
            HeroName(value="spider-man")
