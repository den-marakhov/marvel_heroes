from dataclasses import dataclass
from typing import final

import structlog

from src.application.constants import REFRESH_TOKEN_TYPE
from src.application.exceptions.user import (
    AUTHENTICATION_REQUIRED_MESSAGE,
    InvalidCredentialsError,
    InvalidTokenError,
)
from src.application.interfaces.uow import UnitOfWorkProtocol
from src.application.interfaces.user.token_service import TokenServiceProtocol
from src.application.usecases.users.tokens.delete_user_session_tokens import (
    DeleteUserSessionTokensUseCase,
)
from src.application.usecases.users.tokens.verify_user_session_tokens import (
    VerifyUserSessionTokensUseCase,
)

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class LogoutUseCase:
    token_service: TokenServiceProtocol
    verify_user_session_tokens_usecase: VerifyUserSessionTokensUseCase
    delete_user_session_tokens_usecase: DeleteUserSessionTokensUseCase
    uow: UnitOfWorkProtocol

    async def __call__(self, refresh_token: str) -> None:
        try:
            payload = self.token_service.decode_token(refresh_token)
        except InvalidTokenError as e:
            raise InvalidCredentialsError(AUTHENTICATION_REQUIRED_MESSAGE) from e

        if payload.token_type != REFRESH_TOKEN_TYPE:
            raise InvalidCredentialsError(AUTHENTICATION_REQUIRED_MESSAGE)

        await self.verify_user_session_tokens_usecase(payload)

        async with self.uow:
            user_session = await self.uow.user_sessions.get_user_session_by_id(
                session_id=payload.session_id
            )
            if user_session is not None and user_session.user_id == payload.user_id:
                await self.uow.user_sessions.revoke_session(payload.session_id)
            await self.delete_user_session_tokens_usecase(
                session_id=payload.session_id, user_id=payload.user_id
            )

        logger.info(
            "User has logged out",
            user_id=payload.user_id,
            session_id=payload.session_id,
        )
