from pydantic import BaseModel, ConfigDict, Field


class LoginRequestScheme(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")
