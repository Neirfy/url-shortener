from typing import List
from uuid import UUID, uuid4
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from common.base_model import BaseModel


class URL(BaseModel):
    __tablename__ = "urls"

    id: Mapped[UUID] = mapped_column(
        default_factory=uuid4,
        primary_key=True,
        init=False,
    )
    original_url: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    short_urls: Mapped[List["ShortURL"]] = relationship(  # type: ignore
        "ShortURL",
        back_populates="url",
        cascade="all, delete-orphan",
        init=False,
    )
