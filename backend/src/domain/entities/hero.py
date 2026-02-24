from typing import final
from dataclasses import dataclass,field
from uuid import UUID, uuid4
from datetime import datetime, UTC

from src.domain.value_objects.hero_name import HeroName
from src.domain.exceptions import DomainValidationError

@final
@dataclass(kw_only=True, slots=True)
class HeroEntity:
	
	hero_id: UUID
	name: HeroName
	description: str
	created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
	updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

	def __post_init__(self) -> None:
		
		if len(self.description) > 1000:
			raise DomainValidationError("Description must be at most 1000 characters")
