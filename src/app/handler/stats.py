from fastapi import APIRouter

from app.schema.stats import GetStats
from common.stats import NotFound
from core.database.postgres_connector import CurrentSession
from app.service.stats_service import StatsService

router = APIRouter(
    prefix="/stats",
    tags=["Получение статистики"],
)


@router.get(
    "/{short_id}",
    summary="Количество переходов",
    responses={
        200: {"description": "Количество переходов по ссылке", "model": GetStats},
        404: {"description": "Ссылка не найдена", "model": NotFound},
    },
)
async def upload_archive(
    short_id: str,
    db: CurrentSession,
) -> GetStats:
    """
    Получает количество переходов по короткой ссылке.

    Args:
        short_id (str): Короткий идентификатор ссылки.

    Returns:
        GetStats: Pydantic-модель с полем `visits` — количество переходов.

    Raises:
        HTTPException: Статус 404, если ссылка не найдена.
    """
    service = StatsService(db)
    visits = await service.get_visits_count(short_id)
    return GetStats(visits=visits)
