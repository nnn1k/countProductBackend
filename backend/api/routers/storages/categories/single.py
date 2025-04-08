from fastapi import Depends, APIRouter

from backend.src.core.auth.dependencies import get_user_by_token
from backend.src.core.categories.schemas import CategorySchemaResponse, CategoryCreate
from backend.src.core.storages.dependencies import get_storage_service
from backend.src.core.storages.service import StorageService
from backend.src.core.users.schemas import UserSchema

router = APIRouter(
    prefix="/{category_id}",
)


@router.get('', response_model=CategorySchemaResponse, summary='Посмотреть 1 категорию')
async def get_one_category(
        category_id: int,
        storage_id: int,
        user: UserSchema = Depends(get_user_by_token),
        service: StorageService = Depends(get_storage_service),
):
    category = await service.get_category(user=user, storage_id=storage_id, category_id=category_id)
    return {'category': category}


@router.patch('', response_model=CategorySchemaResponse, summary='Обновить категорию')
async def update_category(
        category_id: int,
        storage_id: int,
        new_category: CategoryCreate,
        user: UserSchema = Depends(get_user_by_token),
        service: StorageService = Depends(get_storage_service),
):
    category = await service.update_category(
        category_id=category_id,
        user=user,
        new_category=new_category,
        storage_id=storage_id
    )
    return {'category': category}


@router.delete('', summary='Удалить категорию')
async def delete_category(
        category_id: int,
        storage_id: int,
        user: UserSchema = Depends(get_user_by_token),
        service: StorageService = Depends(get_storage_service),
):
    await service.delete_category(category_id=category_id, user=user, storage_id=storage_id)
    return {'msg': 'category deleted'}
