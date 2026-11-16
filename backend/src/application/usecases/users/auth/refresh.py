from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from typing import final

import structlog

from src.application.constants import REFRESH_TOKEN_TYPE
from src.application.dtos.token import AuthTokensDTO
from src.application.exceptions.user import (
    AUTHENTICATION_REQUIRED_MESSAGE,
    InvalidCredentialsError,
    InvalidTokenError,
    UserNotFoundError,
)
from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.interfaces.user.session_token_repository import (
    SessionTokenRepositoryProtocol,
)
from src.application.interfaces.user.token_service import TokenServiceProtocol
from src.application.usecases.users.repo.get_user_by_id_from_repo import (
    GetUserFromRepoUseCase,
)
from src.application.usecases.users.tokens.verify_user_session_tokens import (
    VerifyUserSessionTokensUseCase,
)

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class RefreshUseCase:
    get_user_from_repo_usecase: GetUserFromRepoUseCase
    token_service: TokenServiceProtocol
    session_token_repository: SessionTokenRepositoryProtocol
    verify_user_session_tokens_usecase: VerifyUserSessionTokensUseCase
    uow: UnitOfWorkProtocol

    async def __call__(self, refresh_token: str) -> AuthTokensDTO:
        try:
            payload = self.token_service.decode_token(refresh_token)
        except InvalidTokenError as e:
            raise InvalidCredentialsError(AUTHENTICATION_REQUIRED_MESSAGE) from e

        if payload.token_type != REFRESH_TOKEN_TYPE:
            raise InvalidCredentialsError(AUTHENTICATION_REQUIRED_MESSAGE)

        await self.verify_user_session_tokens_usecase(payload)
        try:
            user_dto = await self.get_user_from_repo_usecase(payload.user_id)
        except UserNotFoundError as e:
            raise InvalidCredentialsError(AUTHENTICATION_REQUIRED_MESSAGE) from e

        async with self.uow:
            user_session = await self.uow.user_sessions.get_user_session_by_id(
                session_id=payload.session_id
            )
            now = datetime.now(UTC)
            if (
                user_session is None
                or user_session.revoked_at is not None
                or user_session.user_id != user_dto.user_id
                or user_session.expires_at <= now
            ):
                raise InvalidCredentialsError(AUTHENTICATION_REQUIRED_MESSAGE)

            tokens = self.token_service.create_token_pair(
                user_dto.user_id, payload.session_id
            )
            await self.uow.user_sessions.update_user_session(
                replace(
                    user_session,
                    refresh_jti=tokens.refresh_payload.jti,
                    access_jti=tokens.access_payload.jti,
                    last_seen_at=now,
                    expires_at=now
                    + timedelta(seconds=tokens.refresh_payload.expires_in),
                )
            )
            await self.session_token_repository.save_token_pair(tokens)

        logger.info(
            "Tokens have been refreshed",
            user_id=user_dto.user_id,
            session_id=payload.session_id,
        )
        return tokens
