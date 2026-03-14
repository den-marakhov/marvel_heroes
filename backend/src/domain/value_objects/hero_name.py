from dataclasses import dataclass
from typing import final, ClassVar

from src.domain.exceptions import InvalidHeroNameException


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class HeroName:

	_allowed_values: ClassVar[set[str]] = {
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
	}

	value: str

	def __post_init__(self) -> None:
		if self.value not in self._allowed_values:
			raise InvalidHeroNameException(f"Invalid hero name: {self.value}")
		
		if len(self.value) < 2 or len(self.value) > 100:
			raise InvalidHeroNameException(
				f"Name must be between 2 and 100 characters"
				)
		
	def __str__(self):
			return self.value
