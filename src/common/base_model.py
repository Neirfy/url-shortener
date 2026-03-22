from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    declared_attr,
    mapped_column,
)


class MappedBase(DeclarativeBase):
    """
    Декларативный базовый класс, исходный класс DeclarativeBase,
    существует как родительский класс всех базовых классов или классов моделей данных
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class DateTimeMixin(MappedAsDataclass):
    """Класс данных для mixin даты и времени"""

    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        default_factory=datetime.now,
        sort_order=999,
        comment="Время создания",
    )
    updated_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        init=False,
        onupdate=datetime.now,
        sort_order=999,
        comment="Время обновления",
    )


class DataClassBase(MappedAsDataclass, MappedBase):
    """
    Декларативный класс данных базовый класс
    """

    __abstract__ = True


class BaseModel(DataClassBase, DateTimeMixin):
    """
    Класс - мксин для полей создано и обновлено
    """

    __abstract__ = True
