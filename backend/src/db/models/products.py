from enum import StrEnum

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.db.base import Base, int_pk, created_at, updated_at


class UnitEnum(StrEnum):
    GRAMS = "г"
    KILOGRAMS = "кг"
    LITERS = "л"
    MILLILITERS = "мл"
    PIECES = "шт"
    PACKAGES = "уп"


class ProductOrm(Base):
    __tablename__ = 'products'

    id: Mapped[int_pk]
    name: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    unit: Mapped[UnitEnum] = mapped_column(ENUM(UnitEnum, name='unit_enum'), nullable=True)
    storage_id: Mapped[int] = mapped_column(ForeignKey('storages.id', ondelete='CASCADE'))
    quantity: Mapped[float]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
