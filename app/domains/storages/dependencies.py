from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.storages.repository import StorageRepository
from app.domains.storages.service import StorageService
from app.database.dependencies import get_db
from app.domains.uis.dependencies import get_uis_service
from app.domains.uis.service import UserInStorageService


def get_storage_repo(
        session: AsyncSession = Depends(get_db)
) -> StorageRepository:
    return StorageRepository(session=session)


def get_storage_service(
        repo: StorageRepository = Depends(get_storage_repo),
        uis_serv: UserInStorageService = Depends(get_uis_service),
) -> StorageService:
    return StorageService(storage_repo=repo, uis_serv=uis_serv)
