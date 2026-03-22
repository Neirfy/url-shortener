import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.schema.url import CreateUrl
from common.base_model import BaseModel
from app.service.stats_service import StatsService
from app.service.url_service import URLService
from uuid import UUID


TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_pass@localhost:5433/test_db"


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

    await engine.dispose()


# ---------------- ТЕСТЫ ----------------


@pytest.mark.asyncio
async def test_stats_service_counts_visits(session: AsyncSession):
    url_service = URLService(session)
    stats_service = StatsService(session)

    create_url_obj = CreateUrl(original_url="https://example-visits.com")
    short_id, _ = await url_service.create_short_url(create_url_obj)

    short_obj = await url_service.url_crud.get_by_short_id(session, short_id)

    short_url_id: UUID = short_obj.id

    count = await stats_service.get_visits_count(short_id)
    assert count == 0

    for _ in range(3):
        await url_service.stats_crud.create_visit(session, short_url_id=short_url_id)

    count_after = await stats_service.get_visits_count(short_id)
    assert count_after == 3


@pytest.mark.asyncio
async def test_stats_service_raises_for_nonexistent_short_id(session: AsyncSession):
    stats_service = StatsService(session)
    fake_short_id = "ABC123"

    with pytest.raises(Exception) as exc_info:
        await stats_service.get_visits_count(fake_short_id)

    assert "Short URL не найден" in str(exc_info.value)
