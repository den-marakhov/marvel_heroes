from datetime import UTC, datetime
from uuid import uuid4

from src.domain.constants import ADMIN_ROLE
from src.domain.entities.user import UserEntity
from src.domain.value_objects.email import Email
from src.domain.value_objects.role import Role
from src.domain.value_objects.user_name import UserName
from src.infrastructures.db.mappers.user_db_mapper import UserDBMapper


def test_user_db_mapper_roundtrip() -> None:
    mapper = UserDBMapper()
    now = datetime.now(UTC)
    entity = UserEntity(
        user_id=uuid4(),
        email=Email(value="admin@marvel.local"),
        name=UserName(value="Admin"),
        password_hash="hashed-password",
        role=Role(value=ADMIN_ROLE),
        created_at=now,
        updated_at=now,
    )

    model = mapper.to_model(entity)
    restored = mapper.to_entity(model)

    assert restored.user_id == entity.user_id
    assert restored.email.value == "admin@marvel.local"
    assert restored.name.value == "Admin"
    assert restored.password_hash == "hashed-password"
    assert restored.role.value == ADMIN_ROLE
    assert restored.created_at == now
    assert restored.updated_at == now
