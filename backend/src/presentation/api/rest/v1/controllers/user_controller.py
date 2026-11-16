from contextlib import suppress
from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Cookie, Path, Request, Response, status

from src.application.exceptions.user import (
    AUTHENTICATION_REQUIRED_MESSAGE,
    InvalidCredentialsError,
)
from src.application.usecases.users.auth.login import LoginUseCase
from src.application.usecases.users.auth.logout import LogoutUseCase
from src.application.usecases.users.auth.refresh import RefreshUseCase
from src.application.usecases.users.sessions.get_all_user_sessions_from_repo import (
    GetAllUserSessionsFromRepoUseCase,
)
from src.application.usecases.users.sessions.get_user_sessions_from_repo import (
    GetUserSessionsFromRepoUseCase,
)
from src.application.usecases.users.sessions.revoke_all_user_sessions_from_repo import (
    RevokeAllUserSessionsFromRepoUseCase,
)
from src.application.usecases.users.sessions.revoke_user_session_from_repo import (
    RevokeUserSessionFromRepoUseCase,
)
from src.config.base import Settings
from src.presentation.api.rest.v1.auth_cookies import (
    REFRESH_COOKIE_NAME,
    clear_refresh_cookie,
    set_refresh_cookie,
)
from src.presentation.api.rest.v1.dependencies.auth import CurrentAdmin, CurrentUser
from src.presentation.api.rest.v1.mappers.user_mapper import UserPresentationMapper
from src.presentation.api.rest.v1.schemes.users.requests import LoginRequestScheme
from src.presentation.api.rest.v1.schemes.users.responses import (
    AuthTokensResponseScheme,
    UserSessionResponseScheme,
)

router = APIRouter(prefix="/v1/users", tags=["Users"])


@router.post(
    "/login",
    response_model=AuthTokensResponseScheme,
    summary="log in and issue tokens",
    responses={
        200: {"description": "User has logged in successfully"},
        401: {"description": "Invalid email or password"},
        503: {"description": "Auth storage is unavailable"},
        500: {"description": "Internal server error"},
    },
)
@inject
async def login(
    body: LoginRequestScheme,
    request: Request,
    usecase: FromDishka[LoginUseCase],
    presentation_mapper: FromDishka[UserPresentationMapper],
    settings: FromDishka[Settings],
    response: Response,
) -> AuthTokensResponseScheme:
    ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent") or "unknown"
    login_dto = presentation_mapper.to_login_dto(
        body, ip=ip, user_agent=user_agent
    )
    tokens = await usecase(login_dto)
    set_refresh_cookie(response, tokens.refresh_token, settings)
    return presentation_mapper.to_auth_response(tokens)


@router.post(
    "/refresh",
    response_model=AuthTokensResponseScheme,
    summary="refresh the current session",
    responses={
        200: {"description": "Tokens have been refreshed successfully"},
        401: {"description": "Authentication required"},
        503: {"description": "Auth storage is unavailable"},
        500: {"description": "Internal server error"},
    },
)
@inject
async def refresh(
    usecase: FromDishka[RefreshUseCase],
    presentation_mapper: FromDishka[UserPresentationMapper],
    settings: FromDishka[Settings],
    response: Response,
    refresh_token: Annotated[str | None, Cookie(alias=REFRESH_COOKIE_NAME)] = None,
) -> AuthTokensResponseScheme:
    if refresh_token is None:
        raise InvalidCredentialsError(AUTHENTICATION_REQUIRED_MESSAGE)

    tokens = await usecase(refresh_token=refresh_token)
    set_refresh_cookie(response, tokens.refresh_token, settings)
    return presentation_mapper.to_auth_response(tokens)


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="log out of the current session",
    responses={
        204: {"description": "User has logged out successfully"},
        503: {"description": "Auth storage is unavailable"},
        500: {"description": "Internal server error"},
    },
)
@inject
async def logout(
    usecase: FromDishka[LogoutUseCase],
    settings: FromDishka[Settings],
    response: Response,
    refresh_token: Annotated[str | None, Cookie(alias=REFRESH_COOKIE_NAME)] = None,
) -> None:
    if refresh_token:
        with suppress(InvalidCredentialsError):
            await usecase(refresh_token=refresh_token)

    clear_refresh_cookie(response, settings)


@router.get(
    "/sessions",
    response_model=list[UserSessionResponseScheme],
    summary="get current user sessions",
    responses={
        200: {"description": "User sessions retrieved successfully"},
        401: {"description": "Authentication required"},
        500: {"description": "Internal server error"},
    },
)
@inject
async def get_user_sessions(
    usecase: FromDishka[GetUserSessionsFromRepoUseCase],
    presentation_mapper: FromDishka[UserPresentationMapper],
    current_user: CurrentUser,
):
    user_session_dtos = await usecase(current_user.user_id)
    return presentation_mapper.to_session_response_scheme_list(user_session_dtos)


@router.delete(
    "/sessions",
    summary="revoke all current user sessions",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "User sessions have been revoked successfully"},
        401: {"description": "Authentication required"},
        503: {"description": "Auth storage is unavailable"},
        500: {"description": "Internal server error"},
    },
)
@inject
async def revoke_all_user_sessions(
    usecase: FromDishka[RevokeAllUserSessionsFromRepoUseCase],
    settings: FromDishka[Settings],
    response: Response,
    current_user: CurrentUser,
) -> None:
    await usecase(current_user.user_id)
    clear_refresh_cookie(response, settings)


@router.delete(
    "/sessions/{session_id}",
    summary="revoke user session",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "User session has been revoked successfully"},
        401: {"description": "Authentication required"},
        404: {"description": "User session was not found"},
        500: {"description": "Internal server error"},
    },
)
@inject
async def revoke_user_session(
    usecase: FromDishka[RevokeUserSessionFromRepoUseCase],
    current_user: CurrentUser,
    session_id: UUID = Path(..., description="Session UUID"),
):
    await usecase(user_id=current_user.user_id, session_id=session_id)


@router.get(
    "/sessions/all",
    response_model=list[UserSessionResponseScheme],
    summary="get sessions of all users",
    responses={
        200: {"description": "User sessions retrieved successfully"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        500: {"description": "Internal server error"},
    },
)
@inject
async def get_all_user_sessions(
    usecase: FromDishka[GetAllUserSessionsFromRepoUseCase],
    presentation_mapper: FromDishka[UserPresentationMapper],
    _admin: CurrentAdmin,
) -> list[UserSessionResponseScheme]:
    user_session_dtos = await usecase()
    return presentation_mapper.to_session_response_scheme_list(user_session_dtos)


@router.get(
    "/{user_id}/sessions",
    response_model=list[UserSessionResponseScheme],
    summary="get sessions of a user",
    responses={
        200: {"description": "User sessions retrieved successfully"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        500: {"description": "Internal server error"},
    },
)
@inject
async def get_sessions_of_user(
    usecase: FromDishka[GetUserSessionsFromRepoUseCase],
    presentation_mapper: FromDishka[UserPresentationMapper],
    _admin: CurrentAdmin,
    user_id: UUID = Path(..., description="User UUID"),
) -> list[UserSessionResponseScheme]:
    user_session_dtos = await usecase(user_id)
    return presentation_mapper.to_session_response_scheme_list(user_session_dtos)


@router.delete(
    "/{user_id}/sessions/{session_id}",
    summary="revoke a user session",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "User session has been revoked successfully"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "User session was not found"},
        503: {"description": "Auth storage is unavailable"},
        500: {"description": "Internal server error"},
    },
)
@inject
async def revoke_session_of_user(
    usecase: FromDishka[RevokeUserSessionFromRepoUseCase],
    _admin: CurrentAdmin,
    user_id: UUID = Path(..., description="User UUID"),
    session_id: UUID = Path(..., description="Session UUID"),
) -> None:
    await usecase(user_id=user_id, session_id=session_id)


@router.delete(
    "/{user_id}/sessions",
    summary="revoke all sessions of a user",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "User sessions have been revoked successfully"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        503: {"description": "Auth storage is unavailable"},
        500: {"description": "Internal server error"},
    },
)
@inject
async def revoke_all_sessions_of_user(
    usecase: FromDishka[RevokeAllUserSessionsFromRepoUseCase],
    _admin: CurrentAdmin,
    user_id: UUID = Path(..., description="User UUID"),
) -> None:
    await usecase(user_id)
