from sqlalchemy import Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Refuel(Base):
    """Модель заправки."""

    odometer: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment='Текущий пробег в км.',
    )
    fuel_volume: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment='Объем заправленного бака в литрах',
    )
    is_full: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment='Заправка до полного бака.',
    )
    skipped_previous: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment='Пропущена предыдущая заправка.',
    )
