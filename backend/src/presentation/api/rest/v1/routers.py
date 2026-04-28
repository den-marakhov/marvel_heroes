from fastapi import APIRouter

from src.presentation.api.rest.v1.controllers.hero_controller import (
    router as hero_router,
)

api_v1_router = APIRouter()
api_v1_router.include_router(hero_router)
