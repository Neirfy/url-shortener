import pytest
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from pydantic import ValidationError

from common.base_model import BaseModel as BaseSQL
from app.service.url_service import URLService
from app.model.short_urls import ShortURL
from app.schema.url import CreateUrl

TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_pass@localhost:5433/test_db"


@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(BaseSQL.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(BaseSQL.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine):
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session


# ---------------- ТЕСТЫ ----------------


@pytest.mark.asyncio
async def test_shorten_creates_short_url(session):
    service = URLService(session)
    url_obj = CreateUrl(original_url="https://example.com")
    short_id, _ = await service.create_short_url(url_obj)
    assert isinstance(short_id, str)
    assert len(short_id) == 6


@pytest.mark.asyncio
async def test_shorten_persists_to_db(session):
    service = URLService(session)
    url_obj = CreateUrl(original_url="https://example.com/persist")
    short_id, _ = await service.create_short_url(url_obj)

    short_obj: ShortURL = await service.url_crud.get_by_short_id(session, short_id)
    await session.refresh(short_obj)
    assert short_obj.short_id == short_id
    assert str(short_obj.url.original_url) == str(url_obj.original_url)


@pytest.mark.asyncio
async def test_multiple_shorten_calls(session):
    service = URLService(session)
    urls = ["https://a.com", "https://b.com", "https://c.com"]
    results = []
    for u in urls:
        url_obj = CreateUrl(original_url=u)
        short_id, _ = await service.create_short_url(url_obj)
        results.append(short_id)
    assert len(set(results)) == len(urls)


@pytest.mark.asyncio
async def test_duplicate_url_behavior(session):
    service = URLService(session)
    url_obj = CreateUrl(original_url="https://repeat.com")
    first, _ = await service.create_short_url(url_obj)
    second, _ = await service.create_short_url(url_obj)
    assert first == second


@pytest.mark.asyncio
async def test_invalid_url_raises():
    from pydantic import HttpUrl
    from pydantic import BaseModel

    class URLTestModel(BaseModel):
        url: HttpUrl

    invalid_urls = ["", "htp://bad.url", "example.com"]
    for u in invalid_urls:
        with pytest.raises(ValidationError):
            URLTestModel(url=u)


@pytest.mark.asyncio
async def test_maximum_length_url(session):
    service = URLService(session)
    long_url_obj = CreateUrl(original_url="https://example.com/" + "a" * 2000)
    short_id, _ = await service.create_short_url(long_url_obj)
    assert isinstance(short_id, str)
    assert len(short_id) == 6


@pytest.mark.asyncio
async def test_concurrent_shorten_calls(engine):
    urls = [f"https://concurrent.com/{i}" for i in range(20)]

    async def create_new_session(url):
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as s:
            service = URLService(s)
            url_obj = CreateUrl(original_url=url)
            short_id, _ = await service.create_short_url(url_obj)
            return short_id

    results = await asyncio.gather(*[create_new_session(u) for u in urls])
    assert len(set(results)) == len(urls)
    assert all(isinstance(s, str) for s in results)
