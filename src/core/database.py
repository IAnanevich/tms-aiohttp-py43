from contextlib import asynccontextmanager

from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite+aiosqlite:///messages.db'
Base = declarative_base()


async def init_db(app: web.Application) -> None:
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db(app: web.Application) -> None:
    engine = create_async_engine(DATABASE_URL)
    await engine.dispose()


@asynccontextmanager
async def get_session() -> AsyncSession:
    async_engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session


# engine = create_engine('sqlite:///messages.db')
#
# Session = sessionmaker(bind=engine)
# session = Session()
