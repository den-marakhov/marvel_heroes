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
	full_name: str | None = Field(
		default=None, description="Hero's full name"
	)
	publisher: str | None = Field(
		default=None, description="Comic Publisher (Marvel)"
	)
	uploaded_img_url: str | None = Field(
		default=None ,description="Uploaded image path"
	)
	created_at: datetime = Field(
		..., description="Timestamp when hero record was created (UTC)"
	)
	updated_at: datetime = Field(
		..., description="Timestamp when hero record was updated (UTC)"
	)


class ExternalHeroResponseScheme(BaseModel):

	model_config=ConfigDict(
		extra="forbid",
		frozen=True
	)

	external_id: int = Field(..., description="Hero id from external API")
	name: str = Field(
		...,
		description="Hero name from external API (should be the same as we have in db)"
	)
	full_name: str = Field(
		...,
		description="Hero full name. For example: Peter Parker, Miles Morales etc."
	)
	publisher: str = Field(
		...,
		description="Comics publisher brand. In our case it's Marvel"
	)


	