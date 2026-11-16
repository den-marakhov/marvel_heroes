from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.application.dtos.token import AuthTokensDTO, TokenPayload
from src.application.dtos.user import LoginDTO
from src.application.dtos.user_session import CreateUserSessionDTO
from src.application.exceptions.user import InvalidCredentialsError, UserNotFoundError
from src.application.mappers.user_session import UserSessionDtoEntityMapper
from src.application.usecases.users.auth.login import LoginUseCase
from src.domain.constants import ADMIN_ROLE
from src.domain.entities.user import UserEntity
from src.domain.value_objects.email import Email
from src.domain.value_objects.role import Role
from src.domain.value_objects.user_name import UserName


def _user() -> UserEntity:
    return UserEntity(
        user_id=uuid4(),
        email=Email(value="admin@marvel.local"),
        name=UserName(value="Admin"),
        password_hash="hashed-password",
        role=Role(value=ADMIN_ROLE),
    )


def _login_dto() -> LoginDTO:
    return LoginDTO(
        email="admin@marvel.local",
        password="secretpassword",
        ip="127.0.0.1",
        user_agent="Mozilla/5.0",
    )


def _payload(*, user_id, session_id, jti: str, token_type: str, expires_in: int):
    return TokenPayload(
        user_id=user_id,
        session_id=session_id,
        jti=jti,
        token_type=token_type,  # type: ignore[arg-type]
        expires_in=expires_in,
    )


class TestLoginUseCase:
    @pytest.fixture
    def mock_password_hasher(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def mock_token_service(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def mock_get_user_by_email_from_repo_usecase(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def mock_save_user_session_to_repo_usecase(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def login_usecase(
        self,
        mock_get_user_by_email_from_repo_usecase: AsyncMock,
        mock_password_hasher: MagicMock,
        mock_token_service: MagicMock,
        mock_save_user_session_to_repo_usecase: AsyncMock,
    ) -> LoginUseCase:
        return LoginUseCase(
            get_user_by_email_from_repo_usecase=mock_get_user_by_email_from_repo_usecase,
            password_hasher=mock_password_hasher,
            token_service=mock_token_service,
            mapper=UserSessionDtoEntityMapper(),
            save_user_session_to_repo_usecase=mock_save_user_session_to_repo_usecase,
        )

    @pytest.mark.asyncio
    async def test_login_success(
        self,
        login_usecase: LoginUseCase,
        mock_get_user_by_email_from_repo_usecase: AsyncMock,
        mock_password_hasher: MagicMock,
        mock_token_service: MagicMock,
        mock_save_user_session_to_repo_usecase: AsyncMock,
    ):
        user = _user()
        session_id = uuid4()
        tokens = AuthTokensDTO(
            access_token="access-jwt",
            refresh_token="refresh-jwt",
            access_payload=_payload(
                user_id=user.user_id,
                session_id=session_id,
                jti="access-jti",
                token_type="access",
                expires_in=900,
            ),
            refresh_payload=_payload(
                user_id=user.user_id,
                session_id=session_id,
                jti="refresh-jti",
                token_type="refresh",
                expires_in=2_592_000,
            ),
        )
        mock_get_user_by_email_from_repo_usecase.return_value = user
        mock_password_hasher.verify.return_value = True
        mock_token_service.create_token_pair.return_value = tokens

        before = datetime.now(UTC)
        result = await login_usecase(_login_dto())
        after = datetime.now(UTC)

        assert result is tokens
        mock_get_user_by_email_from_repo_usecase.assert_awaited_once_with(
            "admin@marvel.local"
        )
        mock_password_hasher.verify.assert_awaited_once_with(
            "secretpassword",
            user.password_hash,
        )
        mock_token_service.create_token_pair.assert_called_once()
        call_user_id, call_session_id = mock_token_service.create_token_pair.call_args.args
        assert call_user_id == user.user_id
        assert call_session_id is not None
        mock_save_user_session_to_repo_usecase.assert_awaited_once()
        create_dto, saved_tokens = (
            mock_save_user_session_to_repo_usecase.await_args.args
        )
        assert saved_tokens is tokens
        assert create_dto == CreateUserSessionDTO(
            session_id=call_session_id,
            user_id=user.user_id,
            access_jti="access-jti",
            refresh_jti="refresh-jti",
            ip="127.0.0.1",
            user_agent="Mozilla/5.0",
            expires_at=create_dto.expires_at,
        )
        assert (
            before + timedelta(seconds=2_592_000)
            <= create_dto.expires_at
            <= after + timedelta(seconds=2_592_000)
        )

    @pytest.mark.asyncio
    async def test_login_unknown_email(
        self,
        login_usecase: LoginUseCase,
        mock_get_user_by_email_from_repo_usecase: AsyncMock,
        mock_password_hasher: MagicMock,
        mock_save_user_session_to_repo_usecase: AsyncMock,
    ):
        mock_get_user_by_email_from_repo_usecase.side_effect = UserNotFoundError(
            "User 'admin@marvel.local' has not been found in database"
        )

        with pytest.raises(InvalidCredentialsError):
            await login_usecase(_login_dto())

        mock_password_hasher.verify.assert_not_called()
        mock_save_user_session_to_repo_usecase.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_wrong_password(
        self,
        login_usecase: LoginUseCase,
        mock_get_user_by_email_from_repo_usecase: AsyncMock,
        mock_password_hasher: MagicMock,
        mock_save_user_session_to_repo_usecase: AsyncMock,
    ):
        mock_get_user_by_email_from_repo_usecase.return_value = _user()
        mock_password_hasher.verify.return_value = False

        with pytest.raises(InvalidCredentialsError):
            await login_usecase(_login_dto())

        mock_save_user_session_to_repo_usecase.assert_not_called()
