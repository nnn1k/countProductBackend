from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.products.repository import ProductRepository
from app.domains.products.service import ProductService
from app.database.dependencies import get_db
from app.domains.uis.dependencies import get_uis_service
from app.domains.uis.service import UserInStorageService


def get_product_repo(session: AsyncSession = Depends(get_db)) -> ProductRepository:
    return ProductRepository(session)


def get_product_service(
        product_repo: ProductRepository = Depends(get_product_repo),
        uis_serv: UserInStorageService = Depends(get_uis_service)
) -> ProductService:
    return ProductService(product_repo=product_repo, uis_serv=uis_serv)
