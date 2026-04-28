from dataclasses import dataclass
from types import TracebackType
from typing import final

from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from src.application.interfaces.repositories import HeroRepositoryProtocol
from src.application.interfaces.uow import UnitOfWorkProtocol

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class UnitOfWorkSQLAlchemy(UnitOfWorkProtocol):
    session: AsyncSession
    repository: HeroRepositoryProtocol

    async def __aenter__(self) -> "UnitOfWorkSQLAlchemy":
        logger.debug("Starting database transaction")
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:

        if exc_type is not None:
            logger.warning(
                "Transaction rolled back due to exception: %s - %s",
                exc_type.__name__,
                str(exc_val),
            )
            await self.rollback()

        else:
            await self.commit()

    async def commit(self) -> None:
        logger.debug("Committing transaction")
        await self.session.commit()
        logger.debug("Transaction has been committed successfully")

    async def rollback(self) -> None:

        logger.debug("Rolling back transaction")
        await self.session.rollback()
        logger.debug("Transaction has been rolled back successfully")
