from fastapi import APIRouter

from backend.api.routers.auth.base import router as auth_router
from backend.api.routers.users.base import router as user_router

from backend.api.routers.storages.base import router as base_storage_router
from backend.api.routers.storages.single import router as single_storage_router
from backend.api.routers.storages.users.base import router as user_storage_router

from backend.api.routers.storages.categories.base import router as base_category_storage_router
from backend.api.routers.storages.categories.single import router as single_category_storage_router
from backend.api.routers.storages.categories.products.base import router as base_product_storage_router

from backend.api.routers.test.base import router as test_router

backend_router = APIRouter(
    prefix='/api'
)

# api > auth
backend_router.include_router(auth_router)

# api > users
backend_router.include_router(user_router)

# api > storages > single_storage > users
single_storage_router.include_router(user_storage_router)

# api > storages > single_storage > categories > single_category > products
single_category_storage_router.include_router(base_product_storage_router)

# api > storages > single_storage > categories > single_category
base_category_storage_router.include_router(single_category_storage_router)

# api > storages > single_storage > categories
single_storage_router.include_router(base_category_storage_router)

# api > storages > single_storage
base_storage_router.include_router(single_storage_router)

# api > storages
backend_router.include_router(base_storage_router)

# api > test
backend_router.include_router(test_router)
