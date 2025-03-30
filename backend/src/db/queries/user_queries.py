from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.db.models.users import UserOrm
from backend.src.core.users.schemas import UserSchema


async def get_user_by_id(session: AsyncSession, user_id: int):
    stmt = (
        select(UserOrm)
        .filter_by(id=user_id)
    )
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()
    return UserSchema.model_validate(user, from_attributes=True)
