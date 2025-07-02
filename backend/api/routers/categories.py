from fastapi import APIRouter, Depends

from backend.src.services.auth.dependencies import get_user_by_token
from backend.src.services.categories.dependencies import get_category_service
from backend.src.services.categories.schemas import (
    CategoryCreate,
    CategorySchemaResponse,
    CategoriesSchemaResponse,
)
from backend.src.services.categories.service import CategoryService
from backend.src.services.users.schemas import UserSchema

router = APIRouter(
    tags=["categories"],
    prefix="/storages/{storage_id}/categories",
)


@router.post(
    "",
    response_model=CategorySchemaResponse,
    summary="Создать новую категорию в хранилище",
    description="Хранилище обязательно",
)
async def create_category(
    storage_id: int,
    new_category: CategoryCreate,
    user: UserSchema = Depends(get_user_by_token),
    service: CategoryService = Depends(get_category_service),
):

    category = await service.create(
        new_category=new_category, storage_id=storage_id, user=user
    )
    return {"category": category}


@router.get(
    "",
    response_model=CategoriesSchemaResponse,
    summary="Показать все категории в этом хранилище",
)
async def get_categories(
    storage_id: int,
    user: UserSchema = Depends(get_user_by_token),
    service: CategoryService = Depends(get_category_service),
):
    categories = await service.get_all(storage_id=storage_id, user=user)
    return {"categories": categories}


@router.get(
    "/{category_id}",
    response_model=CategorySchemaResponse,
    summary="Показать конкретную категорию в этом хранилище",
)
async def get_category(
    storage_id: int,
    category_id: int,
    user: UserSchema = Depends(get_user_by_token),
    service: CategoryService = Depends(get_category_service),
):
    category = await service.get_one(
        storage_id=storage_id, category_id=category_id, user=user
    )
    return {"category": category}


@router.put(
    "/{category_id}",
    response_model=CategorySchemaResponse,
    summary="Обновить категорию",
    description="Доступно только владельцу хранилища.",
)
async def update_category(
    storage_id: int,
    category_id: int,
    new_category: CategoryCreate,
    user: UserSchema = Depends(get_user_by_token),
    service: CategoryService = Depends(get_category_service),
):
    category = await service.update(
        storage_id=storage_id, category_id=category_id, new_category=new_category, user=user
    )
    return {"category": category}


@router.delete(
    "/{category_id}",
    summary="Удалить категорию",
    description="Доступно только владельцу хранилища.",
)
async def delete_category(
        storage_id: int,
        category_id: int,
        user: UserSchema = Depends(get_user_by_token),
        service: CategoryService = Depends(get_category_service),
):
    await service.delete(storage_id=storage_id, category_id=category_id, user=user)
    return {"msg": "Категория удалена"}
