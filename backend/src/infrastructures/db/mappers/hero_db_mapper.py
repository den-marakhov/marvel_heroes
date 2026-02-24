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
		)
	
	def to_entity(self, model: HeroModel) -> HeroEntity:
		return HeroEntity(
			hero_id=model.hero_id,
			name=HeroName(value=model.name),
			description=model.description,
			created_at=model.created_at,
			updated_at=model.updated_at,
		)
	
	def update_model_from_entity(
			self,
			model: HeroModel, entity: HeroEntity
			) -> None:
		
		model.name = str(entity.name)
		model.description = entity.description
		model.updated_at = entity.updated_at
		




