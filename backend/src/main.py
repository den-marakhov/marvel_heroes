from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import structlog

from src.application.dtos.user import CreateUserDTO
from src.application.interfaces.user.password_hasher import PasswordHasherProtocol
from src.application.usecases.users.seed_admin import SeedAdminUseCase
from src.config.base import Settings
from src.config.ioc.di import get_providers
from src.config.logging import setup_logging
from src.domain.constants import ADMIN_ROLE
from src.presentation.api.rest.error_handling import setup_exception_handlers
from src.presentation.api.rest.v1.routers import api_v1_router

setup_logging()
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting fastapi app!")
    container: AsyncContainer = app.state.dishka_container
    async with container() as request_container:
        seed_admin = await request_container.get(SeedAdminUseCase)
        password_hasher = await request_container.get(PasswordHasherProtocol)
        settings = await request_container.get(Settings)
        await seed_admin(
            CreateUserDTO(
                email=settings.admin_email,
                name=settings.admin_name,
                role=ADMIN_ROLE,
                password_hash=await password_hasher.hash(settings.admin_password),
            )
        )
    yield
    logger.info("Shutting down fastapi app!")


def create_app() -> FastAPI:

    app = FastAPI(
        title="Marvel Heroes API",
        version="1.0",
        description="Marvel heroes backend app.",
        lifespan=lifespan,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://localhost:8080",
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    container: AsyncContainer = make_async_container(*get_providers())
    setup_dishka(container, app)

    setup_exception_handlers(app)

    app.include_router(api_v1_router, prefix="/api")

    Path("uploads/heroes").mkdir(parents=True, exist_ok=True)

    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

    return app


app = create_app()
