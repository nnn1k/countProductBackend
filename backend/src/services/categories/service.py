from typing import Sequence

from sqlalchemy.exc import IntegrityError

from backend.src.services.categories.repository import CategoryRepository
from backend.src.services.categories.schemas import CategoryCreate, CategorySchema
from backend.src.lib.exc import bad_category_name_exc, category_not_found_exc
from backend.src.services.uis.service import UserInStorageService
from backend.src.services.users.schemas import UserSchema


class CategoryService:

    def __init__(self, category_repo: CategoryRepository, uis_service: UserInStorageService):
        self._category_repo = category_repo
        self._uis_serv = uis_service

    async def create(self, new_category: CategoryCreate, storage_id: int, user: UserSchema) -> CategorySchema:
        await self._uis_serv.check_user_is_owner(user_id=user.id, storage_id=storage_id)
        try:
            category = await self._category_repo.add(
                name=new_category.name,
                description=new_category.description,
                storage_id=storage_id
            )
        except IntegrityError as e:
            print(e)
            raise bad_category_name_exc
        return CategorySchema.model_validate(category)

    async def get_all(self, storage_id: int, user: UserSchema) -> Sequence[CategorySchema]:
        await self._uis_serv.check_user_in_storage(storage_id=storage_id, user_id=user.id)
        categories = await self._category_repo.get_all(storage_id=storage_id)
        return [CategorySchema.model_validate(category) for category in categories]

    async def get_one(self, storage_id: int, category_id: int, user: UserSchema) -> CategorySchema:
        await self._uis_serv.check_user_in_storage(storage_id=storage_id, user_id=user.id)
        category = await self._category_repo.get_one(id=category_id, storage_id=storage_id)
        if not category:
            raise category_not_found_exc
        return CategorySchema.model_validate(category)

    async def update(
            self,
            category_id: int,
            storage_id: int,
            new_category: CategoryCreate,
            user: UserSchema
    ) -> CategorySchema:
        await self._uis_serv.check_user_is_owner(storage_id=storage_id, user_id=user.id)

        try:
            category = await self._category_repo.update(
                category_id=category_id,
                name=new_category.name,
                description=new_category.description
            )
        except IntegrityError:
            raise bad_category_name_exc
        return CategorySchema.model_validate(category)

    async def delete(self, category_id: int, storage_id: int, user: UserSchema) -> None:
        await self._uis_serv.check_user_is_owner(storage_id=storage_id, user_id=user.id)
        category = await self._category_repo.delete(category_id)
        if not category:
            raise category_not_found_exc
