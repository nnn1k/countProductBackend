from fastapi import APIRouter, Depends

from app.domains.storages.service import StorageService
from app.domains.storages.dependencies import get_storage_service
from app.domains.storages.schemas import (
    StorageCreate,
    StorageSchemaResponse,
    StoragesSchemaResponse,
    StorageSchemaRelResponse,
)
from app.domains.auth.dependencies import get_user_by_token
from app.domains.uis.dependencies import get_uis_service
from app.domains.uis.service import UserInStorageService
from app.domains.users.schemas import UserSchema

router = APIRouter(
    tags=["storages"],
    prefix="/storages",
)


@router.post(
    "",
    response_model=StorageSchemaResponse,
    summary="Создать хранилище"
)
async def create_storage(
    new_storage: StorageCreate,
    user: UserSchema = Depends(get_user_by_token),
    service: StorageService = Depends(get_storage_service),
):
    storage = await service.create(new_storage=new_storage, user=user)
    return {"storage": storage}


@router.get(
    "",
    response_model=StoragesSchemaResponse,
    summary="Получить список твоих хранилищ"
)
async def get_all_storage(
    user: UserSchema = Depends(get_user_by_token),
    service: StorageService = Depends(get_storage_service),
):
    storages = await service.get_all(user=user, rel=True)
    return {"storages": storages}


@router.get(
    "/{storage_id}",
    response_model=StorageSchemaRelResponse,
    summary="Получить хранилище",
    description="Работает только если ты являешься участником этого хранилища",
)
async def get_storage(
    storage_id: int,
    user: UserSchema = Depends(get_user_by_token),
    service: StorageService = Depends(get_storage_service),
):

    storage = await service.get_one(user=user, storage_id=storage_id, rel=True)
    return {"storage": storage}


@router.patch(
    "/{storage_id}",
    response_model=StorageSchemaResponse,
    summary="Обновить хранилище",
    description="Доступно только владельцу хранилища.",

)
async def update_storage(
    storage_id: int,
    new_storage: StorageCreate,
    user: UserSchema = Depends(get_user_by_token),
    service: StorageService = Depends(get_storage_service),
):
    storage = await service.update(
        storage_id=storage_id, new_storage=new_storage, user=user
    )
    return {"storage": storage}


@router.delete(
    "/{storage_id}",
    summary="Удалить хранилище",
    description="Доступно только владельцу хранилища.",
)
async def delete_storage(
    storage_id: int,
    user: UserSchema = Depends(get_user_by_token),
    service: StorageService = Depends(get_storage_service),
):
    await service.delete(storage_id=storage_id, user=user)
    return {"msg": "Хранилище удалено"}


@router.post(
    "/join",
    summary="Добавиться в хранилище по коду",
    description="Добавиться в хранилище с помощью кода, добавит только если тебя там до этого не было"
)
async def add_user(
    code: str,
    user: UserSchema = Depends(get_user_by_token),
    service: StorageService = Depends(get_storage_service),
):
    storage = await service.add_user_via_code(code=code, user=user)
    return {"storage": storage}


@router.get(
    "/{storage_id}/users",
    summary="Посмотреть всех пользователей в этом хранилище",
    description="Доступно если ты есть в этом хранилище"
)
async def get_users(
    storage_id: int,
    user: UserSchema = Depends(get_user_by_token),
    service: StorageService = Depends(get_storage_service),
):
    storage = await service.get_one(user=user, storage_id=storage_id, rel=True)
    return {"users": storage.users}


@router.delete(
    "/{storage_id}/users/{user_id}",
    summary="Удалить пользователя из хранилища",
    description="Доступно только владельцу хранилища.",
)
async def remove_user_from_storage(
    storage_id: int,
    user_id: int,
    user: UserSchema = Depends(get_user_by_token),
    service: UserInStorageService = Depends(get_uis_service),
):
    await service.delete_user(storage_id=storage_id, user_id=user_id, user=user)
    return {"msg": "Пользователь удалён"}
