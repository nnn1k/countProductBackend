from typing import List

from sqlalchemy.orm import Mapped, relationship

from app.database.base import Base, int_pk, created_at, updated_at


class UserOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk]
    nickname: Mapped[str]
    email: Mapped[str]
    password: Mapped[bytes]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    storages: Mapped[List['StorageOrm']] = relationship(
        'StorageOrm',
        secondary='users_in_storages',
        back_populates='users',
        lazy='noload'
    )

