from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from common.base_crud import BaseCRUD
from app.model.visits import Visit
from app.model.short_urls import ShortURL


class StatCrud:
    def __init__(self):
        self.visits_crud = BaseCRUD(Visit)

    async def create_visit(self, session: AsyncSession, short_url_id: str) -> Visit:
        visit = await self.visits_crud.create(session, short_url_id=short_url_id)
        return visit

    async def get_visits(self, session: AsyncSession, short_id: str) -> int:
        stmt_url = select(ShortURL.id).where(ShortURL.short_id == short_id)
        result_url = await session.execute(stmt_url)
        short_url_id = result_url.scalar_one_or_none()
        if not short_url_id:
            raise NoResultFound(f"ShortURL с short_id={short_id} не найден")

        stmt_count = select(func.count()).where(Visit.short_url_id == short_url_id)
        result_count = await session.execute(stmt_count)
        return result_count.scalar_one()
