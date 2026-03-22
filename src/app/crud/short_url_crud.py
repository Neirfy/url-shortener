from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from common.base_crud import BaseCRUD
from app.model.short_urls import ShortURL


class ShortURLCrud:
    def __init__(self):
        self.short_crud = BaseCRUD(ShortURL)

    async def get_by_short_id(
        self,
        session: AsyncSession,
        short_id: str,
    ) -> ShortURL | None:
        stmt = (
            select(ShortURL)
            .options(selectinload(ShortURL.url))
            .where(ShortURL.short_id == short_id)
        )
        result = await session.execute(stmt)
        short_obj: ShortURL | None = result.scalar_one_or_none()

        return short_obj
