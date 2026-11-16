import pytest

from src.domain.constants import ADMIN_ROLE, ALLOWED_ROLES
from src.domain.exceptions import InvalidRoleException
from src.domain.value_objects.role import Role


class TestRole:
    def test_role_successful_creation(self):
        for role_name in ALLOWED_ROLES:
            role = Role(value=role_name)
            assert role.value == role_name

    def test_admin_role_constant(self):
        role = Role(value=ADMIN_ROLE)

        assert role.value == "admin"

    def test_role_unsuccessful_creation(self):
        with pytest.raises(InvalidRoleException):
            Role(value="guest")
