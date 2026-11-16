from abc import abstractmethod
from typing import Protocol

from src.application.dtos.user import CreateUserDTO, UserDTO
from src.domain.entities.user import UserEntity


class UserDtoEntityMapperProtocol(Protocol):
    @abstractmethod
    def to_entity_from_create_dto(self, dto: CreateUserDTO) -> UserEntity: ...

    @abstractmethod
    def to_dto(self, entity: UserEntity) -> UserDTO: ...
