from datetime import datetime
from uuid import uuid4

import pytest

from src.domain.constants import ADMIN_ROLE
from src.domain.entities.user import UserEntity
from src.domain.exceptions import DomainValidationError
from src.domain.value_objects.email import Email
from src.domain.value_objects.role import Role
from src.domain.value_objects.user_name import UserName


def _build_user(**overrides) -> UserEntity:
    defaults = {
        "user_id": uuid4(),
        "email": Email(value="admin@marvel.local"),
        "name": UserName(value="Admin"),
        "password_hash": "hashed-password",
        "role": Role(value=ADMIN_ROLE),
    }
    defaults.update(overrides)
    return UserEntity(**defaults)


class TestUserEntity:
    def test_user_entity_success(self):
        user_id = uuid4()
        user = _build_user(user_id=user_id)

        assert user.user_id == user_id
        assert user.email.value == "admin@marvel.local"
        assert user.name.value == "Admin"
        assert user.password_hash == "hashed-password"
        assert user.role.value == ADMIN_ROLE
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_user_entity_empty_password_hash(self):
        with pytest.raises(DomainValidationError):
            _build_user(password_hash="")
