import pytest

from src.domain.exceptions import InvalidUserNameException
from src.domain.value_objects.user_name import UserName


class TestUserName:
    def test_user_name_successful_creation(self):
        user_name = UserName(value="Admin")

        assert user_name.value == "Admin"

    def test_user_name_too_short(self):
        with pytest.raises(InvalidUserNameException):
            UserName(value="A")

    def test_user_name_too_long(self):
        with pytest.raises(InvalidUserNameException):
            UserName(value="A" * 101)
