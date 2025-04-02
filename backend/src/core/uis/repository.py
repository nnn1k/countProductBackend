from typing import Sequence

from sqlalchemy import select, and_, exists, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.src.db.models.storages import StorageOrm
from backend.src.db.models.users_in_storages import UserInStorageOrm


class UserInStorageRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_storages_on_user(self, user_id: int, rel: bool = False) -> Sequence[StorageOrm]:
        stmt = (
            select(StorageOrm)
            .join(UserInStorageOrm)
            .where(
                and_(UserInStorageOrm.user_id == user_id)
            )
        )
        if rel:
            stmt = stmt.options(selectinload(StorageOrm.users))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_one_storage_on_user(self, user_id: int, storage_id: int, rel: bool = False) -> StorageOrm:
        stmt = (
            select(StorageOrm)
            .join(UserInStorageOrm)
            .where(
                and_(
                    UserInStorageOrm.user_id == user_id,
                    UserInStorageOrm.storage_id == storage_id
                )
            )
        )
        if rel:
            stmt = stmt.options(selectinload(StorageOrm.users))
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def check_user_in_storage(self, storage_id: int, user_id: int, is_owner: bool = False) -> bool:
        conditions = [
            UserInStorageOrm.user_id == user_id,
            UserInStorageOrm.storage_id == storage_id,
        ]
        if is_owner:
            conditions.append(UserInStorageOrm.is_owner)
        stmt = select(
            exists()
            .where(
                and_(
                    *conditions
                )
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def add_user_in_storage(self, user_id: int, storage_id: int, is_owner: bool) -> bool:
        stmt = (
            insert(UserInStorageOrm)
            .values(user_id=user_id, storage_id=storage_id, is_owner=is_owner)
        )
        result = await self.session.execute(stmt)
        return bool(result.rowcount)

    async def delete_user(self, user_id: int, storage_id: int) -> bool:
        stmt = (
            delete(UserInStorageOrm)
            .where(
                and_(
                    UserInStorageOrm.user_id == user_id,
                    UserInStorageOrm.storage_id == storage_id
                )
            )
        )
        result = await self.session.execute(stmt)
        return bool(result.rowcount)
