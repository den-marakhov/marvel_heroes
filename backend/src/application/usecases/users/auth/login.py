from dataclasses import dataclass
from typing import final
from uuid import uuid4

import structlog

from src.application.dtos.token import AuthTokensDTO
from src.application.dtos.user import LoginDTO
from src.application.exceptions.user import (
    LOGIN_FAILED_MESSAGE,
    InvalidCredentialsError,
    UserNotFoundError,
)
from src.application.interfaces.user.password_hasher import PasswordHasherProtocol
from src.application.interfaces.user.token_service import TokenServiceProtocol
from src.application.interfaces.user_session.mappers import (
    UserSessionDtoEntityMapperProtocol,
)
from src.application.usecases.users.repo.get_user_by_email_from_repo import (
    GetUserByEmailFromRepoUseCase,
)
from src.application.usecases.users.sessions.save_user_session_to_repo import (
    SaveUserSessionToRepoUseCase,
)

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class LoginUseCase:
    get_user_by_email_from_repo_usecase: GetUserByEmailFromRepoUseCase
    password_hasher: PasswordHasherProtocol
    token_service: TokenServiceProtocol
    mapper: UserSessionDtoEntityMapperProtocol
    save_user_session_to_repo_usecase: SaveUserSessionToRepoUseCase

    async def __call__(self, dto: LoginDTO) -> AuthTokensDTO:
        try:
            user_dto = await self.get_user_by_email_from_repo_usecase(dto.email)
        except UserNotFoundError as e:
            raise InvalidCredentialsError(LOGIN_FAILED_MESSAGE) from e

        if not await self.password_hasher.verify(dto.password, user_dto.password_hash):
            raise InvalidCredentialsError(LOGIN_FAILED_MESSAGE)

        session_id = uuid4()
        tokens = self.token_service.create_token_pair(user_dto.user_id, session_id)
        create_user_session_dto = self.mapper.to_create_dto(
            dto,
            session_id=session_id,
            user_id=user_dto.user_id,
            access_payload=tokens.access_payload,
            refresh_payload=tokens.refresh_payload,
        )
        await self.save_user_session_to_repo_usecase(create_user_session_dto, tokens)
        logger.info(
            "User has logged in",
            user_id=user_dto.user_id,
            session_id=session_id,
        )
        return tokens
