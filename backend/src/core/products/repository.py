from typing import Sequence, Optional

from sqlalchemy import insert, select, and_, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.db.models.products import ProductOrm
from backend.src.lib.classes.enum_classes.unitenum import UnitEnum


class ProductRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, name: str, category_id: int, unit: UnitEnum,
                  storage_id: int, quantity: float, recommended: float):
        stmt = (
            insert(ProductOrm)
            .values(name=name, category_id=category_id, unit=unit,
                    storage_id=storage_id, quantity=quantity, recommended=recommended)
            .returning(ProductOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all(self, storage_id: int, category_id: Optional[int]) -> Sequence[ProductOrm]:
        conditions = [ProductOrm.storage_id == storage_id]
        if category_id:
            conditions.append(ProductOrm.category_id == category_id)
        stmt = (
            select(ProductOrm)
            .where(and_(*conditions))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_one(self, product_id: int) -> ProductOrm:
        stmt = (
            select(ProductOrm)
            .where(
                and_(
                    ProductOrm.id == product_id,
                )
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update(self, product_id: int, name: str, category_id: int, unit: UnitEnum,
                     quantity: float, recommended: float) -> ProductOrm:
        stmt = (
            update(ProductOrm)
            .where(and_(ProductOrm.id == product_id))
            .values(name=name, category_id=category_id, unit=unit, quantity=quantity, recommended=recommended)
            .returning(ProductOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def delete(self, product_id: int) -> ProductOrm:
        stmt = (
            delete(ProductOrm)
            .where(and_(ProductOrm.id == product_id))
            .returning(ProductOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
