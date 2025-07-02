from typing import Optional, Sequence

from sqlalchemy import insert, select, exists, and_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.db.models.categories import CategoryOrm


class CategoryRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, name: str, description: str, storage_id: int) -> CategoryOrm:
        stmt = (
            insert(CategoryOrm)
            .values(name=name, description=description, storage_id=storage_id)
            .returning(CategoryOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all(self, **kwargs) -> Sequence[CategoryOrm]:
        stmt = (
            select(CategoryOrm)
            .filter_by(**kwargs)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_one(self, **kwargs) -> CategoryOrm:
        stmt = (
            select(CategoryOrm)
            .filter_by(**kwargs)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update(self, category_id: int, name: str, description: str) -> CategoryOrm:
        stmt = (
            update(CategoryOrm)
            .where(and_(CategoryOrm.id == category_id))
            .values(name=name, description=description)
            .returning(CategoryOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def delete(self, category_id: int) -> CategoryOrm:
        stmt = (
            delete(CategoryOrm)
            .where(and_(CategoryOrm.id == category_id))
            .returning(CategoryOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
