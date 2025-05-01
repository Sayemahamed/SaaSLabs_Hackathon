import logging
from typing import Any, AsyncGenerator

from API.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

logger = logging.getLogger(__name__)

async_engine: AsyncEngine = create_async_engine(
    url=settings.POSTGRES_URL_ASYNC,
    echo=False,  # Set to False for production, True for debugging
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    pool_timeout=settings.POOL_TIMEOUT,
    pool_recycle=settings.POOL_RECYCLE,
)

async_session_maker = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db() -> None:
    """Initializes the database by creating all tables defined by SQLModel models."""
    logger.info("Initializing database schema...")
    async with async_engine.begin() as conn:
        try:
            from API.db.models import User  # noqa F401 - Explicitly import all models

            await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("Database schema initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize database schema: {e}", exc_info=True)
            raise  # Re-raise the exception to signal failure


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    """Dependency function that yields an async session."""
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()  # Ensure session is closed
