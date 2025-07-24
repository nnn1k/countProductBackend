from fastapi import APIRouter, Depends

from app.domains.auth.dependencies import get_user_by_token
from app.domains.products.dependencies import get_product_service
from app.domains.products.schemas import ProductSchemaResponse, ProductCreate, ProductsSchemaResponse
from app.domains.products.service import ProductService
from app.domains.users.schemas import UserSchema

router = APIRouter(
    tags=["products"],
    prefix="/storages/{storage_id}/products",
)


@router.post(
    "",
    response_model=ProductSchemaResponse,
    summary="Добавить продукт в категорию",
)
async def create_product(
    storage_id: int,
    category_id: int,
    new_product: ProductCreate,
    user: UserSchema = Depends(get_user_by_token),
    service: ProductService = Depends(get_product_service)
):
    product = await service.create(category_id=category_id, storage_id=storage_id, new_product=new_product, user=user)
    return {"product": product}


@router.get(
    "",
    response_model=ProductsSchemaResponse,
    summary="Посмотреть все продукты в категории",
)
async def get_products(
    storage_id: int,
    category_id: int,
    user: UserSchema = Depends(get_user_by_token),
    service: ProductService = Depends(get_product_service)
):
    products = await service.get_all(category_id=category_id, storage_id=storage_id, user=user)
    return {"products": products}


@router.get(
    "/{product_id}",
    response_model=ProductSchemaResponse,
    summary="Посмотреть один продукт в категории"
)
async def get_product(
    product_id: int,
    storage_id: int,
    user: UserSchema = Depends(get_user_by_token),
    service: ProductService = Depends(get_product_service)
):
    product = await service.get_one(product_id=product_id, storage_id=storage_id, user=user)
    return {"product": product}


@router.put(
    "/{product_id}",
    response_model=ProductSchemaResponse,
    summary="Обновить продукт"
)
async def update_product(
        product_id: int,
        storage_id: int,
        new_product: ProductCreate,
        user: UserSchema = Depends(get_user_by_token),
        service: ProductService = Depends(get_product_service)
):
    product = await service.update(
        new_product=new_product, user=user, product_id=product_id, storage_id=storage_id
    )
    return {"product": product}


@router.delete(
    "/{product_id}",
    summary="Удалить продукт"
)
async def delete_product(
        product_id: int,
        storage_id: int,
        user: UserSchema = Depends(get_user_by_token),
        service: ProductService = Depends(get_product_service)
):
    await service.delete(product_id=product_id, storage_id=storage_id, user=user)
    return {"msg": "Продукт удалён"}
