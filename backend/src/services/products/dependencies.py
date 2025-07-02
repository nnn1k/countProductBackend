from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.services.products.repository import ProductRepository
from backend.src.services.products.service import ProductService
from backend.src.db.dependencies import get_db
from backend.src.services.uis.dependencies import get_uis_service
from backend.src.services.uis.service import UserInStorageService


def get_product_repo(session: AsyncSession = Depends(get_db)) -> ProductRepository:
    return ProductRepository(session)


def get_product_service(
        product_repo: ProductRepository = Depends(get_product_repo),
        uis_serv: UserInStorageService = Depends(get_uis_service)
) -> ProductService:
    return ProductService(product_repo=product_repo, uis_serv=uis_serv)
