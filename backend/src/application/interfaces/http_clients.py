from abc import abstractmethod
from typing import Protocol

from src.application.dtos.hero import ExternalAPIHeroDTO


class ExternalMarvelApiProtocol(Protocol):
    @abstractmethod
    async def fetch_hero_by_name(self, name: str) -> list[ExternalAPIHeroDTO]: ...

    @abstractmethod
    async def fetch_hero_by_external_id(
        self, external_id: int
    ) -> ExternalAPIHeroDTO: ...
