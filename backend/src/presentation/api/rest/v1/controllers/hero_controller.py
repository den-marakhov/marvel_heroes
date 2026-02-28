from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Path, status

from src.application.usecases.save_hero_to_repo import ManualHeroCreationInRepoUseCase
from src.application.usecases.get_hero_by_id_from_repo import GetHeroFromRepoUseCase
from src.application.usecases.get_heroes_from_repo import GetHeroesFromRepoUseCase
from src.application.usecases.delete_hero_from_repo import DeleteHeroFromRepoUseCase

from src.presentation.api.rest.v1.schemes.responses import HeroResponseScheme
from src.presentation.api.rest.v1.schemes.requests import HeroRequestBodyScheme
from src.presentation.api.rest.v1.mappers.hero_mapper import HeroPresentationMapper

router = APIRouter(prefix="/v1/heroes", tags=["Heroes"])

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

