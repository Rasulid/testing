
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Создаем асинхронную сессию
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Базовая модель для SQLAlchemy
Base = declarative_base()

# Dependency для получения сессии
async def get_db():
    async with async_session() as session:
        yield session