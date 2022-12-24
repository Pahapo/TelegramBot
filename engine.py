from typing import Union

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.orm import sessionmaker


def create_async_engine(url) -> AsyncEngine:
    return _create_async_engine(url=url, echo=True, encoding='utf-8')


async def proceed_schemas(engine: AsyncEngine, metadata):
    async with engine.connect() as conn:
        await conn.run_sync(metadata.create_all)


def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine,expire_on_commit=False, class_=AsyncSession)
