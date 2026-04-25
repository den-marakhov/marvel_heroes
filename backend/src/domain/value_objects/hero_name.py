from dataclasses import dataclass
from typing import final

from src.domain.exceptions import InvalidHeroNameException

from src.domain.constants import ALLOWED_NAMES

@final
@dataclass(frozen=True, kw_only=True, slots=True)
class HeroName:

	value: str

	def __post_init__(self) -> None:
		if self.value not in ALLOWED_NAMES:
			raise InvalidHeroNameException(f"Invalid hero name: {self.value}")
		
		if len(self.value) < 2 or len(self.value) > 100:
			raise InvalidHeroNameException(
				f"Name must be between 2 and 100 characters"
				)
		
	def __str__(self):
			return self.value
