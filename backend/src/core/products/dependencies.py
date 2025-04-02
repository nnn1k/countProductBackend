from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.products.repository import ProductRepository
from backend.src.core.products.service import ProductService
from backend.src.db.dependencies import get_db


def get_product_repo(session: AsyncSession = Depends(get_db)) -> ProductRepository:
    return ProductRepository(session)


def get_product_service(product_repo: ProductRepository = Depends(get_product_repo)) -> ProductService:
    return ProductService(product_repo)
