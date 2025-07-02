from typing import Sequence

from sqlalchemy.exc import IntegrityError

from backend.src.services.products.repository import ProductRepository
from backend.src.services.products.schemas import ProductSchema, ProductCreate
from backend.src.lib.exc import bad_product_name_exc, product_not_found_exc
from backend.src.services.uis.service import UserInStorageService
from backend.src.services.users.schemas import UserSchema


class ProductService:

    def __init__(self, product_repo: ProductRepository, uis_serv: UserInStorageService):
        self.product_repo = product_repo
        self._uis_serv = uis_serv

    async def create(
        self,
        category_id: int,
        storage_id: int,
        new_product: ProductCreate,
        user: UserSchema,
    ) -> ProductSchema:
        await self._uis_serv.check_user_is_owner(storage_id=storage_id, user_id=user.id)
        try:
            product = await self.product_repo.add(
                    storage_id=storage_id,
                    category_id=category_id,
                    name=new_product.name,
                    unit=new_product.unit,
                    quantity=new_product.quantity,
                    recommended=new_product.recommended,
                )
        except IntegrityError:
            raise bad_product_name_exc
        return ProductSchema.model_validate(product)

    async def get_all(self, category_id: int, storage_id: int, user: UserSchema) -> Sequence[ProductSchema]:
        await self._uis_serv.check_user_in_storage(storage_id=storage_id, user_id=user.id)
        products = await self.product_repo.get_all(storage_id=storage_id, category_id=category_id)
        return [ProductSchema.model_validate(product) for product in products]

    async def get_one(self, product_id: int, storage_id: int, user: UserSchema) -> ProductSchema:
        await self._uis_serv.check_user_in_storage(storage_id=storage_id, user_id=user.id)
        product = await self.product_repo.get_one(product_id=product_id)
        return ProductSchema.model_validate(product)

    async def update(
        self,
        new_product: ProductCreate,
        storage_id: int,
        product_id: int,
        user: UserSchema,
    ) -> ProductSchema:
        await self._uis_serv.check_user_in_storage(storage_id=storage_id, user_id=user.id)
        product = await self.product_repo.update(
            product_id=product_id,
            name=new_product.name,
            unit=new_product.unit,
            quantity=new_product.quantity,
            recommended=new_product.recommended,
        )
        return ProductSchema.model_validate(product)

    async def delete(self, product_id: int, storage_id: int, user: UserSchema) -> None:
        await self._uis_serv.check_user_in_storage(storage_id=storage_id, user_id=user.id)
        product = await self.product_repo.delete(product_id=product_id)
        if not product:
            raise product_not_found_exc
