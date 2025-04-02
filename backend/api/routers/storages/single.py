from fastapi import APIRouter, Depends

from backend.src.core.auth.dependencies import get_user_by_token
from backend.src.core.storages.dependencies import get_storage_service
from backend.src.core.storages.schemas import (
    StorageCreate,
    StorageSchemaResponse,
    StorageSchemaRelResponse
)
from backend.src.core.storages.service import StorageService
from backend.src.core.users.schemas import UserSchema

router = APIRouter(
    prefix="/{storage_id}",
    tags=["storages"],
)


@router.get('', response_model=StorageSchemaRelResponse, summary='Получить хранилище (если ты в нём есть)')
async def get_storage_views(
        storage_id: int,
        user: UserSchema = Depends(get_user_by_token),
        service: StorageService = Depends(get_storage_service)
):

    storage = await service.get_one(user=user, storage_id=storage_id, rel=True)
    return {'storage': storage}


@router.patch('', response_model=StorageSchemaResponse, summary='Обновить хранилище')
async def update_storage_views(
        storage_id: int,
        new_storage: StorageCreate,
        user: UserSchema = Depends(get_user_by_token),
        service: StorageService = Depends(get_storage_service)
):
    storage = await service.update(storage_id=storage_id, new_storage=new_storage, user=user)
    return {'storage': storage}


@router.delete('', summary='Удалить хранилище')
async def delete_storage_views(
        storage_id: int,
        user: UserSchema = Depends(get_user_by_token),
        service: StorageService = Depends(get_storage_service)
):
    await service.delete(storage_id=storage_id, user=user)
    return {'msg': 'storage deleted'}
