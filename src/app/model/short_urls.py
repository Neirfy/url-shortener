from typing import List
from uuid import UUID, uuid4
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model.urls import URL

from app.model.visits import Visit
from common.base_model import BaseModel


class ShortURL(BaseModel):
    __tablename__ = "short_urls"

    id: Mapped[UUID] = mapped_column(
        default_factory=uuid4, primary_key=True, init=False
    )
    short_id: Mapped[str] = mapped_column(
        String(10), unique=True, index=True, nullable=False
    )
    url_id: Mapped[UUID] = mapped_column(ForeignKey("urls.id"), nullable=False)

    url: Mapped[URL] = relationship(
        "URL",
        back_populates="short_urls",
        init=False,
    )
    visits: Mapped[List[Visit]] = relationship(
        "Visit",
        back_populates="short_url",
        cascade="all, delete-orphan",
        init=False,
    )
