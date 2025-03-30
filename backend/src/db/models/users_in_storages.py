from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.db.base import Base, int_pk, created_at, updated_at


class UserInStorageOrm(Base):
    __tablename__ = 'users_in_storages'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    storage_id: Mapped[int] = mapped_column(ForeignKey('storages.id', ondelete='CASCADE'), primary_key=True)
    is_owner: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
