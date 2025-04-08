from sqlalchemy.exc import IntegrityError

from backend.src.core.products.repository import ProductRepository
from backend.src.core.products.schemas import ProductSchema, ProductCreate


class ProductService:

    def __init__(self, product_repo: ProductRepository) -> None:
        self.product_repo = product_repo

    async def create(self, new_product: ProductCreate, storage_id: int, category_id: int) -> ProductSchema:
        product = await self.product_repo.add(
                storage_id=storage_id,
                category_id=category_id,
                name=new_product.name,
                unit=new_product.unit,
                quantity=new_product.quantity,
                recommended=new_product.recommended,
            )
        return ProductSchema.model_validate(product)
