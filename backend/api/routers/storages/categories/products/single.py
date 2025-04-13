from fastapi import APIRouter, Depends

from backend.src.core.auth.dependencies import get_user_by_token
from backend.src.core.storages.dependencies import get_storage_service
from backend.src.core.storages.service import StorageService
from backend.src.core.users.schemas import UserSchema

router = APIRouter(
    prefix='/{product_id}'
)


@router.get('')
async def get_product(
        product_id: int,
        category_id: int,
        storage_id: int,
        user: UserSchema = Depends(get_user_by_token),
        service: StorageService = Depends(get_storage_service)
):
    ...