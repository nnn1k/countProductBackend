from sqlalchemy import select, or_, insert
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.db.models.users import UserOrm


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_login(self, email: str, nickname: str) -> UserOrm:
        stmt = (
            select(UserOrm)
            .where(
                or_(
                    UserOrm.email == email,
                    UserOrm.nickname == nickname
                ),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def register(self, email: str, nickname: str, hashed_password: bytes) -> UserOrm:
        stmt = (
            insert(UserOrm)
            .values(
                nickname=nickname,
                email=email,
                password=hashed_password
            )
            .returning(UserOrm)
        )
        res = await self.session.execute(stmt)
        return res.scalars().first()
