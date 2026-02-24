from abc import abstractmethod
from typing import Protocol
from uuid import UUID


from src.domain.entities.hero import HeroEntity


class HeroRepositoryProtocol(Protocol):

	@abstractmethod
	async def get_heroes(self) -> list[HeroEntity]:
		...

	@abstractmethod
	async def get_hero_by_id(
		self, hero_id: UUID
		) -> HeroEntity | None:
		...

	@abstractmethod
	async def save_hero(
		self, hero_entity: HeroEntity
	) -> None:
		...

	@abstractmethod
	async def delete_hero(
		self, hero_id: UUID
	) -> None:
		...