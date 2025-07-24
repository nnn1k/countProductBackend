from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models.users import UserOrm


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, rel: bool = False, **kwargs) -> UserOrm:
        stmt = (
            select(UserOrm)
            .filter_by(**kwargs)
        )
        if rel:
            stmt = stmt.options(selectinload(UserOrm.storages))
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()
