import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


class DatabaseSettings(BaseSettings):
    """Настройки подключения к PostgreSQL."""

    POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', '')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'postgres')
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT: str = os.getenv('POSTGRES_PORT', '5432')

    class Config:
        """Конфигурация Pydantic для обработки настроек."""

        extra = 'ignore'  # Игнорировать дополнительные переменные


class BotSettings(BaseSettings):
    """Настройки Telegram бота."""

    TOKEN: str = os.getenv('TOKEN', '')
    """Токен бота, обязательный параметр"""

    class Config:
        """Конфигурация Pydantic для обработки настроек."""

        extra = 'ignore'


class Settings(DatabaseSettings, BotSettings):
    """Общие настройки приложения."""

    class Config:
        """Конфигурация Pydantic для обработки настроек."""

        extra = 'ignore'


settings = Settings()

# Настройка подключения к базе данных
SQLALCHEMY_DATABASE_URL = (
    f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@'
    f'{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}'
)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный генератор сессий БД.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy

    Гарантирует закрытие сессии после завершения работы.

    """
    async with AsyncSessionLocal() as session:
        yield session
