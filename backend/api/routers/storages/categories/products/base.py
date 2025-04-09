from fastapi import APIRouter, Depends

from backend.src.core.auth.dependencies import get_user_by_token
from backend.src.core.products.schemas import ProductCreate, ProductSchemaResponse
from backend.src.core.storages.dependencies import get_storage_service
from backend.src.core.storages.service import StorageService
from backend.src.core.users.schemas import UserSchema

router = APIRouter(
    prefix="/products",
)


@router.post('', response_model=ProductSchemaResponse, summary='Создать продукты')
async def create_product(
        storage_id: int,
        category_id: int,
        new_product: ProductCreate,
        user: UserSchema = Depends(get_user_by_token),
        service: StorageService = Depends(get_storage_service)
):
    product = await service.add_product(
        category_id=category_id,
        storage_id=storage_id,
        new_product=new_product,
        user=user
    )
    return {'product': product}
