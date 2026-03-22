from fastapi import APIRouter
from core.config import settings
from app.handler.stats import router as stats_v1
from app.handler.url import router as url_v1


route = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)

route.include_router(url_v1)
route.include_router(stats_v1)
