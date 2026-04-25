from dataclasses import dataclass
from typing import final
from datetime import datetime
from uuid import UUID

from src.domain.constants import ALLOWED_NAMES
from src.domain.exceptions import InvalidHeroNameException

@final
@dataclass(frozen=True, kw_only=True, slots=True)
class HeroNameDTO:
	value: str

	def __post_init__(self):
		if self.value not in ALLOWED_NAMES:
			raise InvalidHeroNameException(
				f"Invalid hero name in HeroDTO"
			)

@final
@dataclass(frozen=True, kw_only=True, slots=True)
class ManualCreateHeroDTO:
	name: HeroNameDTO
	description: str

@final
@dataclass(frozen=True, kw_only=True, slots=True)
class HeroDTO:
	hero_id: UUID
	name: HeroNameDTO
	description: str
	created_at: datetime
	updated_at: datetime
	external_id: int | None = None
	full_name: str | None = None
	publisher: str | None = None
	uploaded_img_url: str | None = None


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class ExternalAPIHeroDTO:
	external_id: int
	name: str
	full_name: str
	publisher: str

@final
@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateHeroDTO:
	name: HeroNameDTO | None = None
	description: str | None = None
	external_id: int | None = None
	full_name: str | None = None
	publisher: str | None = None
	uploaded_img_url: str | None = None
	


