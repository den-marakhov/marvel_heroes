from abc import abstractmethod
from typing import Any, Protocol

from src.application.dtos.hero import HeroDTO


class SerializationMapperProtocol(Protocol):
    @abstractmethod
    def to_dict(self, hero_dto: HeroDTO) -> dict[str, Any]: ...

    @abstractmethod
    def from_dict(self, data: dict[str, Any]) -> HeroDTO: ...

    @abstractmethod
    def to_dict_list(self, dtos: list[HeroDTO]) -> list[dict[str, Any]]: ...

    @abstractmethod
    def from_dict_list(self, data: list[dict[str, Any]]) -> list[HeroDTO]: ...
