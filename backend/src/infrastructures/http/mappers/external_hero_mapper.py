from dataclasses import dataclass
from typing import final

from src.application.dtos.hero import ExternalAPIHeroDTO


@final
@dataclass(frozen=True, slots=True)
class ExternalHeroAPIMapper:
    def to_dto(self, data: dict) -> ExternalAPIHeroDTO:
        return ExternalAPIHeroDTO(
            external_id=int(data["id"]),
            name=data["name"],
            full_name=data["biography"]["full-name"],
            publisher=data["biography"]["publisher"],
        )

    def to_dto_list(self, data: list[dict]) -> list[ExternalAPIHeroDTO]:
        return [self.to_dto(hero) for hero in data]
