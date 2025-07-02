from fastapi import APIRouter

from backend.api.routers.auth import router as auth_router
from backend.api.routers.users import router as user_router
from backend.api.routers.storages import router as base_storage_router
from backend.api.routers.test import router as test_router
from backend.api.routers.categories import router as category_router
from backend.api.routers.products import router as product_router

backend_router = APIRouter(
    prefix='/api'
)


backend_router.include_router(auth_router)

backend_router.include_router(user_router)

backend_router.include_router(base_storage_router)

backend_router.include_router(category_router)

backend_router.include_router(product_router)

backend_router.include_router(test_router)
