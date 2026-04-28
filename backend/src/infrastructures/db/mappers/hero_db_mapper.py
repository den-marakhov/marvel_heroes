from dataclasses import dataclass
from typing import final

from src.domain.entities.hero import HeroEntity
from src.domain.value_objects.hero_name import HeroName
from src.infrastructures.db.models.hero import HeroModel


@final
@dataclass(frozen=True, slots=True)
class HeroDBMapper:
    def to_model(self, entity: HeroEntity) -> HeroModel:
        return HeroModel(
            hero_id=entity.hero_id,
            name=str(entity.name),
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            external_id=entity.external_id,
            full_name=entity.full_name,
            publisher=entity.publisher,
            uploaded_img_url=entity.uploaded_img_url,
        )

    def to_entity(self, model: HeroModel) -> HeroEntity:
        return HeroEntity(
            hero_id=model.hero_id,
            name=HeroName(value=model.name),
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
            external_id=model.external_id,
            full_name=model.full_name,
            publisher=model.publisher,
            uploaded_img_url=model.uploaded_img_url,
        )

    def update_model_from_entity(self, model: HeroModel, entity: HeroEntity) -> None:

        model.name = entity.name.value
        model.description = entity.description
        model.updated_at = entity.updated_at
        model.external_id = entity.external_id
        model.full_name = entity.full_name
        model.publisher = entity.publisher
        model.uploaded_img_url = entity.uploaded_img_url
