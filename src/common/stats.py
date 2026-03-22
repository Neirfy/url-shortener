from pydantic import BaseModel
from fastapi import status


class NotFound(BaseModel):
    error: int = status.HTTP_404_NOT_FOUND
    detail: str = "Ссылка не найдена"
