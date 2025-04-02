from fastapi import Depends, APIRouter

from backend.src.core.auth.dependencies import get_user_by_token
from backend.src.core.categories.schemas import CategorySchemaResponse, CategoryCreate, CategoriesSchemaResponse
from backend.src.core.storages.dependencies import get_storage_service
from backend.src.core.storages.service import StorageService
from backend.src.core.users.schemas import UserSchema

router = APIRouter(
    prefix="/categories",
)


@router.post('', response_model=CategorySchemaResponse, summary='Создать категорию')
async def create_category(
        storage_id: int,
        new_category: CategoryCreate,
        user: UserSchema = Depends(get_user_by_token),
        service: StorageService = Depends(get_storage_service),
):
    category = await service.add_category(storage_id=storage_id, user=user, new_category=new_category)
    return {'category': category}


@router.get('', response_model=CategoriesSchemaResponse, summary='Посмотреть все категории')
async def get_all_category(
        storage_id: int,
        user: UserSchema = Depends(get_user_by_token),
        service: StorageService = Depends(get_storage_service),
):
    categories = await service.get_categories(storage_id=storage_id, user=user)
    return {'categories': categories}
