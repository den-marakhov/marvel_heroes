from dataclasses import dataclass
from typing import final
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.infrastructures.db.exceptions import (
	RepositoryConflictError,
	RepositoryReadError,
	RepositorySaveError
	)

from src.application.interfaces.repositories import HeroRepositoryProtocol
from src.infrastructures.db.mappers.hero_db_mapper import HeroDBMapper

from src.domain.entities.hero import HeroEntity
from src.infrastructures.db.models.hero import HeroModel

@final
@dataclass(frozen=True, slots=True, kw_only=True)
class HeroRepositorySQLAlchemy(HeroRepositoryProtocol):

	session: AsyncSession
	mapper: HeroDBMapper

	async def get_heroes(self) -> list[HeroEntity]:
		
		try:
			stmt = select(HeroModel)
			result = await self.session.execute(stmt)
			hero_models = result.scalars().all()

			return [self.mapper.to_entity(hero_model) for hero_model in hero_models]
		
		except SQLAlchemyError as e:
			raise RepositoryReadError(
				"Failed to retrieve heroes from database"
				) from e
		
	async def get_hero_by_id(
			self, hero_id: UUID
	)-> HeroEntity | None:
		
		try:
			stmt = select(HeroModel).where(HeroModel.hero_id == hero_id)
			result = await self.session.execute(stmt)
			hero_model = result.scalar_one_or_none()

			return self.mapper.to_entity(hero_model) if hero_model else None

		except SQLAlchemyError as e:
			raise RepositoryReadError(
				f"Failed to retrieve hero with id: '{hero_id}' from database"
				) from e
		
	async def update_hero(
			self,
			hero_id: UUID,
			hero_entity: HeroEntity
	)	-> None:
		
		try:
			stmt = select(HeroModel).where(
				HeroModel.hero_id == hero_id
			)
			result = await self.session.execute(stmt)
			hero_model = result.scalar_one_or_none()

			self.mapper.update_model_from_entity(
				hero_model, hero_entity
			) if hero_model else None
		
		except IntegrityError as e:
			raise RepositoryConflictError(
				f"Conflict while saving hero '{hero_entity.hero_id}': {e}"
			) from e
		
		except SQLAlchemyError as e:
			raise RepositorySaveError(
				f"Failed to save hero '{hero_entity.hero_id}': {e}"
			) from e


	async def save_hero(
			self, hero_entity: HeroEntity
	)-> None:
		
		try:
			stmt = select(HeroModel).where(
				HeroModel.name == hero_entity.name.value
			)
			result = await self.session.execute(stmt)
			hero_model = result.scalar_one_or_none()

			if hero_model:
				self.mapper.update_model_from_entity(hero_model, hero_entity)
			else:
				hero_model = self.mapper.to_model(hero_entity)

			self.session.add(hero_model)

		
		except IntegrityError as e:
			raise RepositoryConflictError(
				f"Conflict while saving hero '{hero_entity.hero_id}': {e}"
			) from e
		
		except SQLAlchemyError as e:
			raise RepositorySaveError(
				f"Failed to save hero '{hero_entity.hero_id}': {e}"
			) from e
		
	async def delete_hero(
			self, hero_id: UUID
	) -> None:
		
		try:
			hero_model = await self.session.get(HeroModel, hero_id)

			if hero_model:
				await self.session.delete(hero_model)
					

		except SQLAlchemyError as e:
			raise RepositorySaveError(
				f"Failed to delete hero with id: '{hero_id}': {e}"
			) from e
		
		

			
				


