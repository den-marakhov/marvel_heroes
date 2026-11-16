from dataclasses import dataclass
from typing import final
from uuid import uuid4

from src.application.dtos.user import CreateUserDTO, UserDTO
from src.application.interfaces.user.mappers import UserDtoEntityMapperProtocol
from src.domain.entities.user import UserEntity
from src.domain.value_objects.email import Email
from src.domain.value_objects.role import Role
from src.domain.value_objects.user_name import UserName


@final
@dataclass(frozen=True, slots=True)
class UserDtoEntityMapper(UserDtoEntityMapperProtocol):
    def to_entity_from_create_dto(self, dto: CreateUserDTO) -> UserEntity:
        return UserEntity(
            user_id=uuid4(),
            email=Email(value=dto.email),
            name=UserName(value=dto.name),
            password_hash=dto.password_hash,
            role=Role(value=dto.role),
        )

    def to_dto(self, entity: UserEntity) -> UserDTO:
        return UserDTO(
            user_id=entity.user_id,
            email=entity.email.value,
            name=entity.name.value,
            role=entity.role.value,
            password_hash=entity.password_hash,
        )
