from dataclasses import dataclass
from typing import final

from src.application.constants import ACCESS_TOKEN_TYPE
from src.application.dtos.user import UserDTO
from src.application.exceptions.user import (
    AUTHENTICATION_REQUIRED_MESSAGE,
    InvalidCredentialsError,
    InvalidTokenError,
    UserNotFoundError,
)
from src.application.interfaces.user.token_service import TokenServiceProtocol
from src.application.usecases.users.repo.get_user_by_id_from_repo import (
    GetUserFromRepoUseCase,
)
from src.application.usecases.users.tokens.verify_user_session_tokens import (
    VerifyUserSessionTokensUseCase,
)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class GetCurrentUserUseCase:
    get_user_from_repo_usecase: GetUserFromRepoUseCase
    token_service: TokenServiceProtocol
    verify_user_session_tokens_usecase: VerifyUserSessionTokensUseCase

    async def __call__(self, access_token: str) -> UserDTO:
        try:
            payload = self.token_service.decode_token(access_token)
        except InvalidTokenError as e:
            raise InvalidCredentialsError(AUTHENTICATION_REQUIRED_MESSAGE) from e

        if payload.token_type != ACCESS_TOKEN_TYPE:
            raise InvalidCredentialsError(AUTHENTICATION_REQUIRED_MESSAGE)

        await self.verify_user_session_tokens_usecase(payload)
        try:
            return await self.get_user_from_repo_usecase(payload.user_id)
        except UserNotFoundError as e:
            raise InvalidCredentialsError(AUTHENTICATION_REQUIRED_MESSAGE) from e
