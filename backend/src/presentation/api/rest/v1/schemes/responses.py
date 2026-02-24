from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict



class HeroResponseScheme(BaseModel):

	model_config=ConfigDict(
		frozen=True,
		extra='forbid',
		from_attributes=True
	)

	hero_id: UUID = Field(..., description="Unique hero's identifier")
	name: str = Field(..., description="Hero's name")
	description: str = Field(
		...,
		description="Detailed hero's description. His/her origin, skills, powers etc."
		)
	created_at: datetime = Field(
		..., description="Timestamp when hero record was created (UTC)"
	)
	updated_at: datetime = Field(
		..., description="Timestamp when hero record was updated (UTC)"
	)

	