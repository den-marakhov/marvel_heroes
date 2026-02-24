from uuid import UUID

from sqlalchemy import String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from src.infrastructures.db.models.base import Base

class HeroModel(Base):

	__tablename__ = "heroes"
	__table_args__ = (
		UniqueConstraint("name", name="uq_hero_name"),
	)

	hero_id: Mapped[UUID] = mapped_column(
		PG_UUID(as_uuid=True),
		primary_key=True,
		nullable=False
	)

	name: Mapped[str] = mapped_column(
		String(length=255),
		unique=True,
		nullable=False
	)

	description: Mapped[str] = mapped_column(
		Text, nullable=False
	)


	def __repr__(self) -> str:
		return f"<HeroModel hero_id={self.hero_id} name={self.name}>"
		