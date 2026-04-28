from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import final
from uuid import UUID

from src.domain.exceptions import DomainValidationError, InvalidHeroNameException
from src.domain.value_objects.hero_name import HeroName


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class HeroEntity:
    hero_id: UUID
    name: HeroName
    description: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    external_id: int | None = None
    full_name: str | None = None
    publisher: str | None = None
    uploaded_img_url: str | None = None

    def __post_init__(self) -> None:

        if len(self.description) > 1000:
            raise DomainValidationError("Description must be at most 1000 characters")

        if self.full_name is not None and (
            len(self.full_name) < 2 or len(self.full_name) > 200
        ):
            raise InvalidHeroNameException(
                "Hero full name must be between 2 and 200 characters"
            )
