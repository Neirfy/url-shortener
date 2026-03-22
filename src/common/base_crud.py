from typing import Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

T = TypeVar("T")


class BaseCRUD:
    def __init__(self, model: Type[T]):
        self.model = model

    async def create(self, session: AsyncSession, **kwargs) -> T:
        obj = self.model(**kwargs)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def get(self, session: AsyncSession, id: str) -> T:
        stmt = select(self.model).where(self.model.id == id)
        result = await session.execute(stmt)
        obj = result.scalar_one_or_none()
        if not obj:
            raise NoResultFound(f"{self.model.__name__} с id={id} не найден")
        return obj
