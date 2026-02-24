from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.application.exceptions import (
	HeroNotFoundError,
)

from src.domain.exceptions import (
	DomainValidationError,
	InvalidHeroNameException,
)

def setup_exception_handlers(app: FastAPI) -> None:
	@app.exception_handler(HeroNotFoundError)
	async def hero_not_found_exception_handler(
		request: Request,
		exc: HeroNotFoundError
	) -> JSONResponse:
		return JSONResponse(
			status_code=status.HTTP_404_NOT_FOUND,
			content={"message": str(exc)}
		)
	
	@app.exception_handler(DomainValidationError)
	async def domain_validation_error_handler(
		request: Request,
		exc: DomainValidationError
	) -> JSONResponse:
		return JSONResponse(
			status_code=status.HTTP_400_BAD_REQUEST,
			content={"message": str(exc)},
		)
	
	@app.exception_handler(InvalidHeroNameException)
	async def get_invalid_hero_name_exception_handler(
		request: Request,
		exc: InvalidHeroNameException
	) -> JSONResponse:
		return JSONResponse(
			status_code=status.HTTP_400_BAD_REQUEST,
			content={"message": str(exc)}
		)