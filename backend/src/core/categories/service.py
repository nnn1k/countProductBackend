from typing import Sequence

from sqlalchemy.exc import IntegrityError

from backend.src.core.categories.repository import CategoryRepository
from backend.src.core.categories.schemas import CategoryCreate, CategorySchema
from backend.src.lib.exc import bad_category_name_exc, category_not_found_exc


class CategoryService:

    def __init__(self, category_repo: CategoryRepository) -> None:
        self.category_repo = category_repo

    async def create(self, new_category: CategoryCreate, storage_id: int) -> CategorySchema:
        try:
            category = await self.category_repo.add(
                name=new_category.name,
                description=new_category.description,
                storage_id=storage_id
            )
        except IntegrityError:
            raise bad_category_name_exc
        return CategorySchema.model_validate(category)

    async def get_all(self, storage_id: int) -> Sequence[CategorySchema]:
        categories = await self.category_repo.get_all(storage_id)
        return [CategorySchema.model_validate(category) for category in categories]

    async def get_one(self, storage_id: int, category_id: int) -> CategorySchema:
        category = await self.category_repo.get_one(storage_id, category_id)
        if not category:
            raise category_not_found_exc
        return CategorySchema.model_validate(category)

    async def update(self, new_category: CategoryCreate, category_id: int) -> CategorySchema:
        try:
            category = await self.category_repo.update(
                category_id=category_id,
                name=new_category.name,
                description=new_category.description
            )
        except IntegrityError:
            raise bad_category_name_exc
        return CategorySchema.model_validate(category)

    async def delete(self, category_id: int) -> None:
        category = await self.category_repo.delete(category_id)
        if not category:
            raise category_not_found_exc
