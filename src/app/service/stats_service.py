from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.stats_crud import StatCrud


class StatsService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.stats_crud = StatCrud()

    async def get_visits_count(
        self,
        short_id: str,
    ) -> int:
        print(short_id)
        try:
            count = await self.stats_crud.get_visits(self.session, short_id)
            return count
        except Exception:
            raise HTTPException(status_code=404, detail="Short URL не найден")
