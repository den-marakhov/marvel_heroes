from dataclasses import dataclass
from typing import final

from src.application.dtos.token import AuthTokensDTO
from src.application.dtos.user import LoginDTO
from src.application.dtos.user_session import UserSessionDTO
from src.presentation.api.rest.v1.schemes.users.requests import LoginRequestScheme
from src.presentation.api.rest.v1.schemes.users.responses import (
    AuthTokensResponseScheme,
    UserSessionResponseScheme,
)


@final
@dataclass(frozen=True, slots=True)
class UserPresentationMapper:
    def to_login_dto(
        self, scheme: LoginRequestScheme, ip: str, user_agent: str
    ) -> LoginDTO:
        return LoginDTO(
            email=scheme.email,
            password=scheme.password,
            ip=ip,
            user_agent=user_agent,
        )

    def to_auth_response(self, dto: AuthTokensDTO) -> AuthTokensResponseScheme:
        return AuthTokensResponseScheme(access_token=dto.access_token)

    def to_session_response_scheme(
        self, dto: UserSessionDTO
    ) -> UserSessionResponseScheme:
        return UserSessionResponseScheme(
            session_id=dto.session_id,
            user_id=dto.user_id,
            ip=dto.ip,
            user_agent=dto.user_agent,
            location=dto.location,
            created_at=dto.created_at,
            last_seen_at=dto.last_seen_at,
            expires_at=dto.expires_at,
        )

    def to_session_response_scheme_list(
        self, dtos: list[UserSessionDTO]
    ) -> list[UserSessionResponseScheme]:
        return [self.to_session_response_scheme(dto) for dto in dtos]
