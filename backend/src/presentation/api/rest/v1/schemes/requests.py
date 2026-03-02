from pydantic import BaseModel, Field, ConfigDict


class HeroRequestBodyScheme(BaseModel):

	model_config=ConfigDict(
		extra='forbid',
		frozen=True,
	)

	name: str = Field(..., description="Hero's name")
	description: str = Field(..., description="Hero's brief description")


class HeroUpdateRequestScheme(BaseModel):

	model_config=ConfigDict(
		extra="forbid",
		frozen=True
	)
	
	name: str | None = Field(
		default=None, description="Hero's name"
	)
	description: str | None = Field(
		default=None, description="Hero's brief description"
	)


class EnrichHeroBodyScheme(BaseModel):

	model_config=ConfigDict(
		extra="forbid",
		frozen=True
	)

	external_id: int = Field(..., description="Hero id from external API")