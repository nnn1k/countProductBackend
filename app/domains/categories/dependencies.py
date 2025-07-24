from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.categories.repository import CategoryRepository
from app.domains.categories.service import CategoryService
from app.database.dependencies import get_db
from app.domains.uis.dependencies import get_uis_service
from app.domains.uis.service import UserInStorageService


def get_category_repo(
        session: AsyncSession = Depends(get_db),
) -> CategoryRepository:
    return CategoryRepository(session)


def get_category_service(
        category_repo: CategoryRepository = Depends(get_category_repo),
        uis_service: UserInStorageService = Depends(get_uis_service),
) -> CategoryService:
    return CategoryService(category_repo=category_repo, uis_service=uis_service)

