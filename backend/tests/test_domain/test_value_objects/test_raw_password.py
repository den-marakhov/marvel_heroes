import pytest

from src.domain.exceptions import InvalidPasswordException
from src.domain.value_objects.raw_password import RawPassword


class TestRawPassword:
    def test_raw_password_successful_creation(self):
        password = RawPassword(value="secretpassword")

        assert password.value == "secretpassword"

    def test_raw_password_too_short(self):
        with pytest.raises(InvalidPasswordException):
            RawPassword(value="short")

    def test_raw_password_too_long(self):
        with pytest.raises(InvalidPasswordException):
            RawPassword(value="s" * 129)
