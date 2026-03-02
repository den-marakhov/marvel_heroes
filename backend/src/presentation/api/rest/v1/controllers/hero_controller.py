from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Path, Query, Body, status

from src.application.usecases.repo.save_hero_to_repo import ManualHeroCreationInRepoUseCase
from src.application.usecases.repo.get_hero_by_id_from_repo import GetHeroFromRepoUseCase
from src.application.usecases.repo.get_heroes_from_repo import GetHeroesFromRepoUseCase
from src.application.usecases.repo.delete_hero_from_repo import DeleteHeroFromRepoUseCase

from src.application.usecases.external_api.fetch_heroes_from_external_api import FetchHeroesFromExternalAPIUseCase
from src.application.usecases.external_api.enrich_hero_usecase import EnrichHeroUseCase

from src.presentation.api.rest.v1.schemes.responses import (
	HeroResponseScheme, ExternalHeroResponseScheme
)
from src.presentation.api.rest.v1.schemes.requests import (
	HeroRequestBodyScheme, EnrichHeroBodyScheme
)
from src.presentation.api.rest.v1.mappers.hero_mapper import HeroPresentationMapper

router = APIRouter(prefix="/v1/heroes", tags=["Heroes"])

@router.get(
		"/search",
		response_model=list[ExternalHeroResponseScheme],
		summary="search heroes in external api by hero's name",
)
@inject
async def get_heroes_from_external_api(
	usecase: FromDishka[FetchHeroesFromExternalAPIUseCase],
	presentation_mapper: FromDishka[HeroPresentationMapper],
	name: str = Query(..., description="Hero name for searching in external api"),
):
	heroes = await usecase(hero_name=name)
	return ([
		
			presentation_mapper
			.to_external_api_hero_response_scheme(hero_dto)
			for hero_dto in heroes
		
	])

@router.get(
		"/",
		response_model=list[HeroResponseScheme],
		summary="get all heroes",
		responses={
			200: {"description": "Heroes retrieved successfully"},
      500: {"description": "Internal server error"},
		}
)
@inject
async def get_heroes(
	usecase: FromDishka[GetHeroesFromRepoUseCase],
	presentation_mapper: FromDishka[HeroPresentationMapper]
):
	hero_dtos = await usecase()

	return [
		presentation_mapper.to_response_scheme(hero_dto) for hero_dto in hero_dtos
	]
	

@router.get(
		"/{hero_id}",
		response_model=HeroResponseScheme,
		summary="get hero by id",
		responses={
			200: {"description": "Hero has been retrieved successfully"},
      404: {"description": "Hero was not found"},
      500: {"description": "Internal server error"},
		}
)
@inject
async def get_hero_by_id(
	usecase: FromDishka[GetHeroFromRepoUseCase],
	presentation_mapper: FromDishka[HeroPresentationMapper],
	hero_id: UUID = Path(..., description="Hero UUID")
):
	hero_dto = await usecase(hero_id=hero_id)
	return presentation_mapper.to_response_scheme(hero_dto)


@router.post(
	"/",
	response_model=HeroResponseScheme,
	status_code=status.HTTP_201_CREATED,
	summary="manually create hero",
	responses={
		201: {"description": "Hero has been created successfully"},
		400: {"description": "Bad request"},
		500: {"description": "Internal server error"},
	}
	)
@inject
async def create_hero(
	hero_body: HeroRequestBodyScheme,
	usecase: FromDishka[ManualHeroCreationInRepoUseCase],
	presentation_mapper: FromDishka[HeroPresentationMapper]
) -> HeroResponseScheme:
	
	hero_dto_from_scheme = presentation_mapper.to_manual_hero_create_dto(hero_body)
	hero_dto = await usecase(hero_dto=hero_dto_from_scheme)
	return presentation_mapper.to_response_scheme(hero_dto)

@router.post(
		"/{hero_id}/enrich",
		response_model=HeroResponseScheme,
		summary="enrich hero in db with external API data",
		responses={
			200: {"description": "Hero has been updated with external data successfully"},
			400: {"description": "Bad Request"},
			404: {"description": "Hero was not found"},
			500: {"description": "Internal server error"}
		}
)
@inject
async def enrich_hero_data_from_external_api(
	usecase: FromDishka[EnrichHeroUseCase],
	presentation_mapper: FromDishka[HeroPresentationMapper],
	hero_id: UUID = Path(..., description="Hero UUID"),
	body: EnrichHeroBodyScheme = Body(
		..., description="Request body with external hero id"
	)
):
	hero_dto = await usecase(hero_id=hero_id, external_id=body.external_id)
	return presentation_mapper.to_response_scheme(hero_dto)

@router.delete(
	"/{hero_id}",
	summary="delete hero from database",
	status_code=status.HTTP_204_NO_CONTENT,
	responses={
		204: {"description": "Hero has been deleted successfully"},
		400: {"description": "Bad Request"},
		404: {"description": "Hero was not found"},
		500: {"description": "Internal server error"},
	}
)
@inject
async def delete_hero(
	usecase: FromDishka[DeleteHeroFromRepoUseCase],
	hero_id: UUID = Path(..., description="Hero UUID"),
):
	await usecase(hero_id=hero_id)

