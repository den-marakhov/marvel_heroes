from dataclasses import dataclass, field
from typing import final, Literal
from datetime import datetime, UTC
from uuid import UUID

@final
@dataclass(frozen=True, kw_only=True, slots=True)
class HeroNameDTO:
	value: Literal[
		"Spider-Man",
		"Captain America",
		"Iron Man",
		"Hulk",
		"Thor",
		"Black Widow",
		"Black Panther",
		"Ant-Man",
		"Hawkeye",
		"Scarlet Witch",
		"Vision",
		"Wolverine"
	]

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
	external_img_url: str | None = None
	uploaded_img_url: str | None = None


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class ExternalAPIHeroDTO:
	external_id: int
	name: str
	full_name: str
	publisher: str
	image_url: str

@final
@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateHeroDTO:
	name: HeroDTO | None = None
	description: str | None = None
	external_id: int | None = None
	full_name: str | None = None
	publisher: str | None = None
	external_img_url: str | None = None
	uploaded_img_url: str | None = None
	


