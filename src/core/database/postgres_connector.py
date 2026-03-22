from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from common.base_model import MappedBase
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession


DATABASE_URL = str(settings.db_url)

async_engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_table():
    async with async_engine.begin() as coon:
        await coon.run_sync(MappedBase.metadata.create_all)


async def get_session():
    async with async_session() as session:
        yield session


CurrentSession = Annotated[AsyncSession, Depends(get_session)]
