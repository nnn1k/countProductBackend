from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.categories.repository import CategoryRepository
from backend.src.core.categories.service import CategoryService
from backend.src.db.dependencies import get_db


def get_category_repo(
        session: AsyncSession = Depends(get_db),
) -> CategoryRepository:
    return CategoryRepository(session)


def get_category_service(
        category_repo: CategoryRepository = Depends(get_category_repo),
) -> CategoryService:
    return CategoryService(category_repo)
