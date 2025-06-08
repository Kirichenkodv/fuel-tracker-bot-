from pathlib import Path
from typing import AsyncGenerator

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


class Settings(BaseSettings):
    """Общие настройки приложения."""

    # Настройки DB
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: str = '5432'

    # Настройки бота
    TOKEN: str

    class Config:
        """Конфигурация Pydantic для обработки настроек."""

        # Указываем путь к .env относительно расположения config.py
        env_file = Path(__file__).parent.parent.parent / 'infra' / '.env'
        env_file_encoding = 'utf-8'


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
