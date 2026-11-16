from dataclasses import dataclass
from typing import final

from src.domain.entities.user import UserEntity
from src.domain.value_objects.email import Email
from src.domain.value_objects.role import Role
from src.domain.value_objects.user_name import UserName
from src.infrastructures.db.models.user import UserModel


@final
@dataclass(frozen=True, slots=True)
class UserDBMapper:
    def to_model(self, entity: UserEntity) -> UserModel:
        return UserModel(
            user_id=entity.user_id,
            email=entity.email.value,
            name=entity.name.value,
            password_hash=entity.password_hash,
            role=entity.role.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(self, model: UserModel) -> UserEntity:
        return UserEntity(
            user_id=model.user_id,
            email=Email(value=model.email),
            name=UserName(value=model.name),
            password_hash=model.password_hash,
            role=Role(value=model.role),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def update_model_from_entity(self, model: UserModel, entity: UserEntity) -> None:
        model.email = entity.email.value
        model.name = entity.name.value
        model.password_hash = entity.password_hash
        model.role = entity.role.value
        model.updated_at = entity.updated_at
