from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from common.base_crud import BaseCRUD
from app.model.urls import URL
from app.model.short_urls import ShortURL
import random, string


class URLCrud:
    def __init__(self):
        self.url_crud = BaseCRUD(URL)
        self.short_crud = BaseCRUD(ShortURL)

    async def create_short_url(
        self,
        session: AsyncSession,
        original_url: str,
    ) -> tuple[ShortURL, bool]:
        stmt = select(ShortURL).join(URL).where(URL.original_url == original_url)
        result = await session.execute(stmt)
        existing_short = result.scalar_one_or_none()
        if existing_short:
            return existing_short, False

        stmt_url = select(URL).where(URL.original_url == original_url)
        result_url = await session.execute(stmt_url)
        url = result_url.scalar_one_or_none()
        if not url:
            url = await self.url_crud.create(session, original_url=original_url)

        MAX_ATTEMPTS = 10
        for _ in range(MAX_ATTEMPTS):
            short_id = "".join(
                random.choices(string.ascii_letters + string.digits, k=6)
            )
            try:
                short_url = await self.short_crud.create(
                    session, short_id=short_id, url_id=url.id
                )
                return short_url, True
            except IntegrityError:
                continue

        raise RuntimeError("Не удалось сгенерировать уникальный short_id за 10 попыток")

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
        return result.scalar_one_or_none()
