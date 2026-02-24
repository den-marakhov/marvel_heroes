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
		"Black widow",
		"Black panther",
		"Ant Man",
		"Hawk eye",
		"Wanda",
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

