from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from app.service.url_service import URLService
from app.schema.url import CreateUrl, ShortUrl
from common.stats import NotFound
from core.database.postgres_connector import CurrentSession

router = APIRouter(prefix="/url", tags=["Ссылки"])


@router.post(
    "/shorten",
    summary="Создание короткой ссылки",
    responses={
        200: {
            "description": "Ссылка уже существует",
            "model": ShortUrl,
        },
        201: {
            "description": "Ссылка создана",
            "model": ShortUrl,
        },
    },
)
async def create_short_url(
    url: CreateUrl,
    db: CurrentSession,
):
    """
    Создает короткую ссылку для переданного URL.

    Если URL уже существует в базе, возвращает его с кодом 200.
    Если URL новый — создаёт короткую ссылку и возвращает с кодом 201.

    Args:
        url (HttpUrl): Оригинальный URL для сокращения.

    Returns:
        JSONResponse: Словарь с полями:
            - short_id (str): Короткий идентификатор ссылки.
            - original_url (str): Исходный URL.
        И соответствующий статус-код:
            - 200 — ссылка уже существует
            - 201 — ссылка создана
    """
    service = URLService(db)
    short_url, created = await service.create_short_url(url)
    return JSONResponse(
        content={"short_id": short_url},
        status_code=201 if created else 200,
    )


@router.get(
    "/{short_id}",
    # response_model=str,
    summary="Редирект по ссылке",
    responses={
        200: {
            "description": "",
            "model": str,
        },
        404: {
            "description": "Ссылка не найдена",
            "model": NotFound,
        },
    },
)
async def visit_short_url(
    short_id: str,
    request: Request,
    db: CurrentSession,
):
    """
    Выполняет редирект по короткой ссылке или возвращает оригинальный URL в формате JSON.

    Args:
        short_id (str): Короткий идентификатор ссылки.
        request (Request): HTTP-запрос (для проверки заголовка Accept).

    Returns:
        RedirectResponse: Редирект на оригинальный URL.
        JSONResponse: JSON с полем original_url, если Accept: application/json.

    Raises:
        HTTPException: Статус 404, если короткая ссылка не найдена.
    """
    service = URLService(db)
    try:
        original_url = await service.visit_short_url(short_id)  # возвращает str
    except ValueError:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")

    print(str(original_url))
    if "application/json" in request.headers.get("accept", ""):
        return JSONResponse(str(original_url))
    return RedirectResponse(url=str(original_url))
