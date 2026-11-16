from abc import abstractmethod
from typing import Any, Protocol

from src.application.dtos.user import UserDTO


class UserSerializationMapperProtocol(Protocol):
    @abstractmethod
    def to_dict(self, user_dto: UserDTO) -> dict[str, Any]: ...

    @abstractmethod
    def from_dict(self, data: dict[str, Any]) -> UserDTO: ...
