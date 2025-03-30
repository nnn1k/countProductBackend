from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.db.base import Base, int_pk, created_at, updated_at


class CategoryOrm(Base):
    __tablename__ = 'categories'

    id: Mapped[int_pk]
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    storage_id: Mapped[int] = mapped_column(ForeignKey('storages.id', ondelete='CASCADE'))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    __table_args__ = (
        UniqueConstraint('name', 'storage_id', name='unique_category_name_storage_id'),
    )


class SystemCategoryOrm(Base):
    __tablename__ = 'system_categories'
    id: Mapped[int_pk]
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)

