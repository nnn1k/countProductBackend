from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.db.base import Base, int_pk, created_at, updated_at


class StorageOrm(Base):
    __tablename__ = 'storages'

    id: Mapped[int_pk]
    name: Mapped[str]
    code: Mapped[str] = mapped_column(unique=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    users: Mapped[List['UserOrm']] = relationship(
        'UserOrm',
        secondary='users_in_storages',
        back_populates='storages',
        lazy='noload'
    )

    __table_args__ = (
        UniqueConstraint('name', 'creator_id', name='unique_storage_name_creator_id'),
    )
