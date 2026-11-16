from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AuthTokensResponseScheme(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    access_token: str = Field(..., description="JWT access token")
    token_type: Literal["bearer"] = Field(
        default="bearer",
        description="Token type for the Authorization header",
    )


class UserSessionResponseScheme(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", from_attributes=True)

    session_id: UUID = Field(..., description="Unique session identifier")
    user_id: UUID = Field(..., description="User who owns the session")
    ip: str = Field(..., description="IP address of the session")
    user_agent: str = Field(..., description="User agent of the session")
    location: str | None = Field(default=None, description="Approximate session location")
    created_at: datetime = Field(
        ..., description="Timestamp when the session was created (UTC)"
    )
    last_seen_at: datetime = Field(
        ..., description="Timestamp when the session was last used (UTC)"
    )
    expires_at: datetime = Field(
        ..., description="Timestamp when the session expires (UTC)"
    )
