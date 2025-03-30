from fastapi import APIRouter, Depends

from backend.api.response_schemas import StorageSchemaResponse
from backend.src.core.auth.dependencies import get_user_by_token
from backend.src.core.storages.dependencies import get_storage_service
from backend.src.core.storages.service import StorageService
from backend.src.core.users.schemas import UserSchema

router = APIRouter(
    prefix="/users",
)


@router.post('/via_code', response_model=StorageSchemaResponse,summary='Добавиться в хранилище по коду')
async def add_user_to_code_views(
        code: str,
        user: UserSchema = Depends(get_user_by_token),
        service: StorageService = Depends(get_storage_service)
):
    storage = await service.add_user_via_code(code=code, user=user)
    return {'storage': storage}


@router.delete('/{user_id}', summary='Удалить пользователя из хранилища')
async def delete_user_on_storage_views(
        user_id: int,
        storage_id: int,
        user: UserSchema = Depends(get_user_by_token),
        service: StorageService = Depends(get_storage_service)
):
    await service.delete_user(user_id=user_id, storage_id=storage_id, user=user)
    return {'msg': 'user deleted'}
