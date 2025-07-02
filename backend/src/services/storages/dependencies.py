from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.services.categories.dependencies import get_category_service
from backend.src.services.categories.service import CategoryService
from backend.src.services.products.dependencies import get_product_service
from backend.src.services.products.service import ProductService
from backend.src.services.storages.repository import StorageRepository
from backend.src.services.storages.service import StorageService
from backend.src.db.dependencies import get_db
from backend.src.services.uis.dependencies import get_uis_service
from backend.src.services.uis.service import UserInStorageService


def get_storage_repo(
        session: AsyncSession = Depends(get_db)
) -> StorageRepository:
    return StorageRepository(session=session)


def get_storage_service(
        repo: StorageRepository = Depends(get_storage_repo),
        uis_serv: UserInStorageService = Depends(get_uis_service),
        category_serv: CategoryService = Depends(get_category_service),
        product_serv: ProductService = Depends(get_product_service)
) -> StorageService:
    return StorageService(storage_repo=repo, uis_serv=uis_serv, category_serv=category_serv, product_serv=product_serv)
