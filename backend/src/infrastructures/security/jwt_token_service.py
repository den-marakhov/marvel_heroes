from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Final, final
from uuid import UUID, uuid4

import jwt

from src.application.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from src.application.dtos.token import AuthTokensDTO, TokenPayload
from src.application.exceptions.user import InvalidTokenError
from src.application.interfaces.user.token_service import TokenServiceProtocol
from src.infrastructures.security.mappers.jwt_token_mapper import JwtTokenMapper

JWT_ALGORITHM: Final = "HS256"


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class JwtTokenService(TokenServiceProtocol):
    secret: str
    access_ttl: int
    refresh_ttl: int
    mapper: JwtTokenMapper

    def decode_token(self, token: str) -> TokenPayload:
        try:
            token_data = jwt.decode(
                token, self.secret, algorithms=[JWT_ALGORITHM]
            )
            return self.mapper.to_token_payload(token_data)
        except (jwt.PyJWTError, KeyError, ValueError) as e:
            raise InvalidTokenError("Invalid token") from e

    def create_token_pair(self, user_id: UUID, session_id: UUID) -> AuthTokensDTO:
        now = datetime.now(UTC)
        access_token_data = {
            "sub": str(user_id),
            "sid": str(session_id),
            "jti": str(uuid4()),
            "type": ACCESS_TOKEN_TYPE,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(seconds=self.access_ttl)).timestamp()),
        }
        refresh_token_data = {
            "sub": str(user_id),
            "sid": str(session_id),
            "jti": str(uuid4()),
            "type": REFRESH_TOKEN_TYPE,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(seconds=self.refresh_ttl)).timestamp()),
        }
        tokens = self.mapper.to_auth_tokens_dto(
            access_token=jwt.encode(
                access_token_data, self.secret, algorithm=JWT_ALGORITHM
            ),
            refresh_token=jwt.encode(
                refresh_token_data, self.secret, algorithm=JWT_ALGORITHM
            ),
            access_payload=self.mapper.to_token_payload(access_token_data),
            refresh_payload=self.mapper.to_token_payload(refresh_token_data),
        )
        return tokens  # noqa: RET504
