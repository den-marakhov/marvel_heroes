from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.application.dtos.user import UserDTO
from src.application.exceptions.user import (
    AUTHENTICATION_REQUIRED_MESSAGE,
    InvalidCredentialsError,
)
from src.application.usecases.users.get_current_admin import GetCurrentAdminUseCase
from src.application.usecases.users.get_current_user import GetCurrentUserUseCase

_bearer_scheme = HTTPBearer(auto_error=False)


@inject
async def get_current_user(
    usecase: FromDishka[GetCurrentUserUseCase],
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(_bearer_scheme)
    ],
) -> UserDTO:
    if credentials is None:
        raise InvalidCredentialsError(AUTHENTICATION_REQUIRED_MESSAGE)

    return await usecase(access_token=credentials.credentials)


CurrentUser = Annotated[UserDTO, Depends(get_current_user)]


@inject
async def get_current_admin(
    usecase: FromDishka[GetCurrentAdminUseCase],
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(_bearer_scheme)
    ],
) -> UserDTO:
    if credentials is None:
        raise InvalidCredentialsError(AUTHENTICATION_REQUIRED_MESSAGE)

    return await usecase(access_token=credentials.credentials)


CurrentAdmin = Annotated[UserDTO, Depends(get_current_admin)]
