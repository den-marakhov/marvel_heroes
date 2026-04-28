from dataclasses import dataclass
from typing import final

import httpx
import stamina
import structlog

from src.application.dtos.hero import ExternalAPIHeroDTO
from src.application.exceptions import HeroNotFoundError
from src.application.interfaces.http_clients import ExternalMarvelApiProtocol
from src.infrastructures.http.mappers.external_hero_mapper import ExternalHeroAPIMapper

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class ExternalMarvelHeroApiClient(ExternalMarvelApiProtocol):
    base_url: str
    api_key: str
    client: httpx.AsyncClient
    mapper: ExternalHeroAPIMapper

    @stamina.retry(
        on=(httpx.HTTPStatusError, httpx.RequestError),
        attempts=3,
        wait_initial=0.5,
        wait_jitter=1.0,
        wait_max=10,
    )
    async def fetch_hero_by_name(self, name: str) -> list[ExternalAPIHeroDTO]:
        transformed_name = name.strip().lower().replace("-", "_").replace(" ", "_")
        url = f"{self.base_url}/{self.api_key}/search/{transformed_name}"
        logger.debug("Fetching hero from external api", name=transformed_name, url=url)

        response = await self.client.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("response") == "error":
            logger.warning(
                "Hero not found in external api",
                name=transformed_name,
                error=data.get("error"),
            )
            raise HeroNotFoundError(f"Hero '{name}' not found in external API")

        logger.debug(
            "Heroes have been successfully fetched from external api",
            name=transformed_name,
            count=len(data["results"]),
        )

        return self.mapper.to_dto_list(data["results"])

    @stamina.retry(
        on=(httpx.HTTPStatusError, httpx.RequestError),
        attempts=3,
        wait_initial=0.5,
        wait_jitter=1.0,
        wait_max=10,
    )
    async def fetch_hero_by_external_id(self, external_id: int) -> ExternalAPIHeroDTO:
        url = f"{self.base_url}/{self.api_key}/{external_id}"
        logger.debug(
            "fetching hero from external api", external_id=external_id, url=url
        )

        response = await self.client.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("response") == "error":
            logger.warning(
                "Hero not found in external api",
                external_id=external_id,
                error=data.get("error"),
            )
            raise HeroNotFoundError(
                f"Failed to fetch hero from external API by id: '{external_id}'"
            )

        logger.debug(
            "Hero has been successfully retrieved from external API",
            external_id=external_id,
        )

        return self.mapper.to_dto(data)
