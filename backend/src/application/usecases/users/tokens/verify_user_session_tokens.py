from dataclasses import dataclass
from typing import final

from src.application.constants import ACCESS_TOKEN_TYPE
from src.application.dtos.token import TokenPayload
from src.application.interfaces.user.session_token_repository import (
    SessionTokenRepositoryProtocol,
)
from src.application.usecases.users.tokens.rehydrate_user_session_tokens import (
    RehydrateUserSessionTokensUseCase,
)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class VerifyUserSessionTokensUseCase:
    session_token_repository: SessionTokenRepositoryProtocol
    rehydrate_user_session_tokens_usecase: RehydrateUserSessionTokensUseCase

    async def __call__(self, payload: TokenPayload) -> None:
        stored_token_jti = await (
            self.session_token_repository.get_access_token_jti(payload.session_id)
            if payload.token_type == ACCESS_TOKEN_TYPE
            else self.session_token_repository.get_refresh_token_jti(
                payload.session_id
            )
        )
        if stored_token_jti != payload.jti:
            await self.rehydrate_user_session_tokens_usecase(payload)
