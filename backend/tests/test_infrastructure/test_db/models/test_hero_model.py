from datetime import datetime, UTC
from sqlalchemy import UniqueConstraint, String, Text, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class TestBaseModel(DeclarativeBase):
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		default=lambda: datetime.now(UTC),
		server_default=func.now(),
		nullable=False
	)

	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		default=lambda: datetime.now(UTC),
		onupdate=lambda: datetime.now(UTC),
		nullable=False
	)


class TestHeroModel(TestBaseModel):
		__tablename__ = "heroes"
		__table_args__ = (
		UniqueConstraint("name", name="uq_hero_name"),
	)
		
		hero_id: Mapped[str] = mapped_column(
			String(length=36),
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

		full_name: Mapped[str | None] = mapped_column(
			String(200), nullable=True
		)

		publisher: Mapped[str | None] = mapped_column(
			String(100), nullable=True
		)

		uploaded_img_url: Mapped[str | None] = mapped_column(
			Text, nullable=True
		)

		external_id: Mapped[int | None] = mapped_column(
			Integer, nullable=True
		)

		def __repr__(self) -> str:
			return f"<TestHeroModel hero_id={self.hero_id} name={self.name}>"
