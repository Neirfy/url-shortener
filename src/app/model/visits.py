from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from common.base_model import BaseModel


class Visit(BaseModel):
    __tablename__ = "visits"

    id: Mapped[UUID] = mapped_column(
        default_factory=uuid4,
        primary_key=True,
        init=False,
    )
    short_url_id: Mapped[UUID] = mapped_column(
        ForeignKey("short_urls.id"),
        nullable=False,
    )
    visited_at: Mapped[datetime] = mapped_column(
        DateTime,
        default_factory=datetime.now,
        init=False,
    )

    short_url: Mapped["ShortURL"] = relationship(  # type: ignore
        "ShortURL",
        back_populates="visits",
        init=False,
    )
