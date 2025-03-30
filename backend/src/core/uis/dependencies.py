from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.db.dependencies import get_db
from backend.src.core.uis.repository import UserInStorageRepository
from backend.src.core.uis.service import UserInStorageService


def get_uis_repo(
        session: AsyncSession = Depends(get_db)
) -> UserInStorageRepository:
    return UserInStorageRepository(session)


def get_uis_service(
        uis_repo: UserInStorageRepository = Depends(get_uis_repo)
) -> UserInStorageService:
    return UserInStorageService(uis_repo)
