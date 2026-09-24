
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine,async_sessionmaker
from app.core.config import get_settings

Base=declarative_base()
settings=get_settings()


engine=create_async_engine(
    settings.database_url,
            future=True,
            echo=False,
            pool_size=20,
            max_overflow=10
            )

async_session=async_sessionmaker(engine,expire_on_commit=False,class_=AsyncSession)

async def get_db():
    async with async_session() as session:
        yield session

