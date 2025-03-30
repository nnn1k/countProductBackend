from fastapi import APIRouter

from backend.api.routers.auth import router as auth_router
from backend.api.routers.users import router as user_router

from backend.api.routers.storages.base import router as base_storage_router
from backend.api.routers.storages.single import router as single_storage_router
from backend.api.routers.storages.users import router as user_storage_router
from backend.api.routers.storages.categories import router as category_storage_router


from backend.api.routers.test import router as test_router

backend_router = APIRouter(
    prefix='/api'
)


backend_router.include_router(auth_router)

single_storage_router.include_router(user_storage_router)
single_storage_router.include_router(category_storage_router)

base_storage_router.include_router(single_storage_router)
backend_router.include_router(base_storage_router)

backend_router.include_router(user_router)

backend_router.include_router(test_router)
