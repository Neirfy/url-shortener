from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union

from app.crud.short_url_crud import ShortURLCrud
from app.crud.stats_crud import StatCrud
from app.crud.url_crud import URLCrud
from app.model.short_urls import ShortURL
from app.schema.url import CreateUrl


class URLService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.url_crud = URLCrud()
        self.short_url_crud = ShortURLCrud()
        self.stats_crud = StatCrud()

    async def create_short_url(
        self,
        url: CreateUrl,
    ) -> Union[ShortURL, None]:
        short_id, created = await self.url_crud.create_short_url(
            self.session, str(url.original_url)
        )
        return short_id.short_id, created

    async def visit_short_url(
        self,
        short_id: str,
    ) -> Union[str, None]:
        short_obj: ShortURL | None = await self.short_url_crud.get_by_short_id(
            self.session, short_id
        )
        if not short_obj:
            raise HTTPException(status_code=404, detail="Short URL не найден")

        await self.stats_crud.create_visit(self.session, short_obj.id)

        return short_obj.url.original_url
