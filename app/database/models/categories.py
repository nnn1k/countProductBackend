from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, int_pk, created_at, updated_at


class CategoryOrm(Base):
    __tablename__ = 'categories'

    id: Mapped[int_pk]
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    storage_id: Mapped[int] = mapped_column(ForeignKey('storages.id', ondelete='CASCADE'))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    storage: Mapped['StorageOrm'] = relationship(
        'StorageOrm',
        back_populates='categories',
        lazy='noload'
    )

    __table_args__ = (
        UniqueConstraint('name', 'storage_id', name='unique_category_name_storage_id'),
    )


