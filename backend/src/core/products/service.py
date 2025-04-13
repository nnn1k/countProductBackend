from typing import Sequence

from sqlalchemy.exc import IntegrityError

from backend.src.core.products.repository import ProductRepository
from backend.src.core.products.schemas import ProductSchema, ProductCreate
from backend.src.lib.exc import bad_product_name_exc, product_not_found_exc


class ProductService:

    def __init__(self, product_repo: ProductRepository) -> None:
        self.product_repo = product_repo

    async def create(self, new_product: ProductCreate, storage_id: int, category_id: int) -> ProductSchema:
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

    async def get_all(self, storage_id: int, category_id: int) -> Sequence[ProductSchema]:
        products = await self.product_repo.get_all(storage_id=storage_id, category_id=category_id)
        return [ProductSchema.model_validate(product) for product in products]

    async def get_one(self, product_id: int) -> ProductSchema:
        product = await self.product_repo.get_one(product_id=product_id)
        return ProductSchema.model_validate(product)

    async def update(self, product_id: int, category_id: int,  new_product: ProductCreate) -> ProductSchema:
        product = await self.product_repo.update(
            product_id=product_id,
            name=new_product.name,
            unit=new_product.unit,
            quantity=new_product.quantity,
            recommended=new_product.recommended,
            category_id=category_id,
        )
        return ProductSchema.model_validate(product)

    async def delete(self, product_id: int) -> None:
        product = await self.product_repo.delete(product_id=product_id)
        if not product:
            raise product_not_found_exc
