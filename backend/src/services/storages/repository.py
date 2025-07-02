from sqlalchemy import insert, select, and_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.src.db.models.storages import StorageOrm


class StorageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, name: str, code: str, creator_id: int) -> StorageOrm:
        stmt = (
            insert(StorageOrm)
            .values(name=name, code=code, creator_id=creator_id)
            .returning(StorageOrm)
        )
        result = await self.session.execute(stmt)
        storage = result.scalars().first()
        return storage

    async def get_one(self, rel: bool = False, **kwargs) -> StorageOrm:
        stmt = select(StorageOrm).filter_by(**kwargs)
        if rel:
            stmt = stmt.options(selectinload(StorageOrm.users))
            stmt = stmt.options(selectinload(StorageOrm.categories))
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update(self, storage_id: int, **kwargs) -> StorageOrm:
        stmt = (
            update(StorageOrm)
            .where(and_(StorageOrm.id == storage_id))
            .values(**kwargs)
            .returning(StorageOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def delete(self, storage_id: int) -> StorageOrm:
        stmt = (
            delete(StorageOrm)
            .where(and_(StorageOrm.id == storage_id))
            .returning(StorageOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
