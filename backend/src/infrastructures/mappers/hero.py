from dataclasses import dataclass
from datetime import datetime
from typing import Any, final
from uuid import UUID

from src.application.dtos.hero import HeroDTO, HeroNameDTO
from src.application.interfaces.serialization import SerializationMapperProtocol


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class HeroSerializationMapper(SerializationMapperProtocol):
    def to_dict(self, hero_dto: HeroDTO) -> dict[str, Any]:

        return {
            "hero_id": str(hero_dto.hero_id),
            "name": hero_dto.name.value,
            "description": hero_dto.description,
            "created_at": hero_dto.created_at.isoformat(),
            "updated_at": hero_dto.updated_at.isoformat(),
            "external_id": hero_dto.external_id,
            "full_name": hero_dto.full_name,
            "publisher": hero_dto.publisher,
            "uploaded_img_url": hero_dto.uploaded_img_url,
        }

    def from_dict(self, data: dict[str, Any]) -> HeroDTO:

        return HeroDTO(
            hero_id=UUID(data["hero_id"]),
            name=HeroNameDTO(value=data["name"]),
            description=data["description"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            external_id=data["external_id"],
            full_name=data["full_name"],
            publisher=data["publisher"],
            uploaded_img_url=data["uploaded_img_url"],
        )

    def to_dict_list(self, dtos: list[HeroDTO]) -> list[dict[str, Any]]:

        return [self.to_dict(dto) for dto in dtos]

    def from_dict_list(self, data: list[dict[str, Any]]) -> list[HeroDTO]:

        return [self.from_dict(hero) for hero in data]
