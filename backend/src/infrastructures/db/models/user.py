from uuid import UUID

from sqlalchemy import String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructures.db.models.base import Base
from src.infrastructures.db.models.user_session import UserSessionModel


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_user_email"),)

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, nullable=False
    )

    email: Mapped[str] = mapped_column(String(length=254), unique=True, nullable=False)

    name: Mapped[str] = mapped_column(String(length=100), nullable=False)

    password_hash: Mapped[str] = mapped_column(Text, nullable=False)

    role: Mapped[str] = mapped_column(String(length=50), nullable=False)

    user_sessions: Mapped[list[UserSessionModel]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<UserModel user_id={self.user_id} email={self.email}>"
