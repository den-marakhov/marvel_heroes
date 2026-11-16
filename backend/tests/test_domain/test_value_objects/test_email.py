import pytest

from src.domain.exceptions import InvalidEmailException
from src.domain.value_objects.email import Email


class TestEmail:
    def test_email_successful_creation(self):
        email = Email(value="Admin@Marvel.Local")

        assert email.value == "admin@marvel.local"

    def test_email_without_at_sign(self):
        with pytest.raises(InvalidEmailException):
            Email(value="admin.marvel.local")

    def test_email_without_domain_dot(self):
        with pytest.raises(InvalidEmailException):
            Email(value="admin@marvel")
