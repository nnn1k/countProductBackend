from typing import Sequence

from sqlalchemy.exc import IntegrityError

from backend.src.core.categories.schemas import CategoryCreate, CategorySchema
from backend.src.core.categories.service import CategoryService
from backend.src.core.products.schemas import ProductCreate, ProductSchema
from backend.src.core.products.service import ProductService
from backend.src.core.storages.repository import StorageRepository
from backend.src.core.storages.schemas import StorageSchema, StorageSchemaRel, StorageCreate
from backend.src.core.users.schemas import UserSchema
from backend.src.core.uis.service import UserInStorageService
from backend.src.lib.exc import (
    bad_generation_code_exc,
    user_in_storage_not_exist_exc,
    bad_storage_name_exc,
    storage_not_found_exc
)
from backend.src.lib.utils import get_random_code


class StorageService:
    def __init__(
            self,
            storage_repo: StorageRepository,
            uis_serv: UserInStorageService,
            category_serv: CategoryService,
            product_serv: ProductService,
    ) -> None:
        self._storage_repo = storage_repo
        self._uis_serv = uis_serv
        self._category_serv = category_serv
        self._product_serv = product_serv

    async def create(self, new_storage: StorageCreate, user: UserSchema) -> StorageSchema:
        code = await self._generate_unique_storage_code()
        try:
            storage = await self._storage_repo.add(name=new_storage.name, code=code, creator_id=user.id)
        except IntegrityError:
            raise bad_storage_name_exc

        await self._uis_serv.add_user(
            user_id=user.id,
            storage_id=storage.id,
            is_owner=True
        )
        return StorageSchema.model_validate(storage)

    async def get_all(
            self,
            user: UserSchema,
            rel: bool = False
    ) -> Sequence[StorageSchemaRel] | Sequence[StorageSchema]:
        return await self._uis_serv.get_all_storages_on_user(user_id=user.id, rel=rel)

    async def get_one(
            self,
            user: UserSchema,
            storage_id: int,
            rel: bool = False,
    ) -> StorageSchema | StorageSchemaRel:
        storage = await self._uis_serv.get_one_storage_on_user(user=user, rel=rel, storage_id=storage_id)
        if not storage:
            raise user_in_storage_not_exist_exc
        return storage

    async def update(self, storage_id: int, new_storage: StorageCreate, user: UserSchema) -> StorageSchema:
        await self._uis_serv.check_user_is_owner(storage_id=storage_id, user_id=user.id)
        try:
            storage = await self._storage_repo.update(storage_id=storage_id, name=new_storage.name)
        except IntegrityError:
            raise bad_storage_name_exc
        if not storage:
            raise user_in_storage_not_exist_exc
        return StorageSchema.model_validate(storage)

    async def delete(self, storage_id: int, user: UserSchema) -> None:
        await self._uis_serv.check_user_is_owner(user_id=user.id, storage_id=storage_id)
        storage = await self._storage_repo.delete(storage_id=storage_id)
        if not storage:
            raise storage_not_found_exc

    async def _generate_unique_storage_code(self, min_length: int = 4, max_length: int = 8, attempts: int = 5) -> str:
        for length in range(min_length, max_length + 1):
            for _ in range(attempts):
                code = get_random_code(k=length)
                storage = await self._storage_repo.get_one(code=code)
                if not storage:
                    return code

        raise bad_generation_code_exc

    async def add_user_via_code(self, code: str, user: UserSchema) -> StorageSchema:
        storage = await self._storage_repo.get_one(code=code)
        if not storage:
            raise storage_not_found_exc
        await self._uis_serv.add_user(user_id=user.id, storage_id=storage.id)
        return StorageSchema.model_validate(storage)

    async def delete_user(self, storage_id: int, user_id: int, user: UserSchema) -> None:
        await self._uis_serv.delete_user(user=user, user_id=user_id, storage_id=storage_id)

    async def add_category(self, storage_id: int, new_category: CategoryCreate, user: UserSchema) -> CategorySchema:
        await self._uis_serv.check_user_is_owner(user_id=user.id, storage_id=storage_id)
        return await self._category_serv.create(new_category=new_category, storage_id=storage_id)

    async def get_categories(self, user: UserSchema, storage_id: int) -> Sequence[CategorySchema]:
        await self._uis_serv.check_user_in_storage(storage_id=storage_id, user_id=user.id)
        return await self._category_serv.get_all(storage_id=storage_id)

    async def get_category(self, user: UserSchema, storage_id: int, category_id: int) -> CategorySchema:
        await self._uis_serv.check_user_in_storage(storage_id=storage_id, user_id=user.id)
        return await self._category_serv.get_one(storage_id=storage_id, category_id=category_id)

    async def update_category(
            self,
            category_id: int,
            storage_id: int,
            new_category: CategoryCreate,
            user: UserSchema
    ) -> CategorySchema:
        await self._uis_serv.check_user_is_owner(storage_id=storage_id, user_id=user.id)
        return await self._category_serv.update(new_category=new_category, category_id=category_id)

    async def delete_category(self, category_id: int, storage_id: int, user: UserSchema) -> None:
        await self._uis_serv.check_user_is_owner(storage_id=storage_id, user_id=user.id)
        await self._category_serv.delete(category_id=category_id)

    async def add_product(
            self,
            category_id: int,
            storage_id: int,
            new_product: ProductCreate,
            user: UserSchema
    ) -> ProductSchema:
        await self._uis_serv.check_user_is_owner(storage_id=storage_id, user_id=user.id)
        return await self._product_serv.create(new_product=new_product, category_id=category_id, storage_id=storage_id)

    async def get_products(self, category_id: int, storage_id: int, user: UserSchema) -> Sequence[ProductSchema]:
        await self._uis_serv.check_user_in_storage(storage_id=storage_id, user_id=user.id)
        return await self._product_serv.get_all(category_id=category_id, storage_id=storage_id)

    async def get_product(self, product_id: int, storage_id: int, user: UserSchema) -> ProductSchema:
        await self._uis_serv.check_user_in_storage(storage_id=storage_id, user_id=user.id)
        return await self._product_serv.get_one(product_id=product_id)

    async def update_product(
            self, new_product: ProductCreate, category_id: int, storage_id: int, product_id: int, user: UserSchema
    ) -> ProductSchema:
        await self._uis_serv.check_user_in_storage(storage_id=storage_id, user_id=user.id)
        return await self._product_serv.update(product_id=product_id, new_product=new_product, category_id=category_id)

    async def delete_product(self, product_id: int, storage_id: int, user: UserSchema) -> None:
        await self._uis_serv.check_user_in_storage(storage_id=storage_id, user_id=user.id)
        await self._product_serv.delete(product_id=product_id)
