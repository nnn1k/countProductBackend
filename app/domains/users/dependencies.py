from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.users.repository import UserRepository
from app.domains.users.service import UserService
from app.database.dependencies import get_db


def get_user_repo(
        session: AsyncSession = Depends(get_db)
):
    return UserRepository(session)


def get_user_service(
        user_repo: UserRepository = Depends(get_user_repo)
):
    return UserService(user_repo)
