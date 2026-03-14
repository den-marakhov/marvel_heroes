from typing import final
from dataclasses import dataclass

import structlog


from src.application.interfaces.http_clients import ExternalMarvelApiProtocol
from src.application.dtos.hero import ExternalAPIHeroDTO
from src.application.exceptions import ( 
	HeroNotFoundError,
	FailedFetchHeroFromExternalAPIException
)

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class FetchHeroesFromExternalAPIUseCase:
			
		marvel_hero_api_client: ExternalMarvelApiProtocol

		async def __call__(self, hero_name: str) -> list[ExternalAPIHeroDTO]:
				logger.info(
						"Starting to fetch heroes from external API",
						hero_name=hero_name
					)
				
				try:
					heroes =( 
						await self.marvel_hero_api_client.fetch_hero_by_name(hero_name)
					)
					logger.info(
						"Heroes have been fetched from external API",
						hero_name=hero_name
					)
					return heroes

				except HeroNotFoundError as e:
					logger.error(
						"Unable to find heroes in external API service",
						hero_name=hero_name,
						error=str(e)
					)
					raise

				except Exception as e:
					logger.exception(
						"Failed to fetch heroes from external API",
						hero_name=hero_name,
						error=str(e)
					)
					raise FailedFetchHeroFromExternalAPIException(
						"Couldn't fetch heroes from external service"
					) from e

	
