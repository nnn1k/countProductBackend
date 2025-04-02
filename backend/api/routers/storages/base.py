from typing import List

from fastapi import APIRouter, Depends

from backend.src.core.storages.service import StorageService
from backend.src.core.storages.dependencies import get_storage_service
from backend.src.core.storages.schemas import (
    StorageCreate,
    StorageSchemaResponse,
    StoragesSchemaResponse
)
from backend.src.core.users.schemas import UserSchema
from backend.src.core.auth.dependencies import get_user_by_token

router = APIRouter(
    tags=['storages'],
    prefix='/storages',
)


@router.post('', response_model=StorageSchemaResponse, summary='Создать хранилище')
async def create_storage_views(
        new_storage: StorageCreate,
        user: UserSchema = Depends(get_user_by_token),
        service: StorageService = Depends(get_storage_service)
):
    storage = await service.create(new_storage=new_storage, user=user)
    return {'storage': storage}


@router.get('', response_model=StoragesSchemaResponse, summary='Получить список хранилищ')
async def get_all_storage_views(
        user: UserSchema = Depends(get_user_by_token),
        service: StorageService = Depends(get_storage_service)
):
    storages = await service.get_all(user=user, rel=True)
    return {'storages': storages}


