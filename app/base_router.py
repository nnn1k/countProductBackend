from fastapi import APIRouter, Depends

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.database.recreate import recreate

from app.domains.auth.routes import router as auth_router
from app.domains.users.routes import router as user_router
from app.domains.storages.routes import router as base_storage_router
from app.domains.categories.routes import router as category_router
from app.domains.products.routes import router as product_router

backend_router_v1 = APIRouter(
    prefix='/api/v1'
)

test_router = APIRouter(
    prefix="/test",
    tags=["test"],
)

backend_router_v1.include_router(auth_router)

backend_router_v1.include_router(user_router)

backend_router_v1.include_router(base_storage_router)

backend_router_v1.include_router(category_router)

backend_router_v1.include_router(product_router)


@test_router.get('/test_db', summary='Проверка подключения бд')
async def get_test_db(
        session: AsyncSession = Depends(get_db)
):
    res = await session.execute(text('SELECT EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)::int'))
    result = res.scalars().first()
    return {
        "ok": True
    }


@test_router.get('/recreate', summary='Дроп бд')
async def recreate_db():
    await recreate()
    return {
        'msg': 'Recreate database successfully'
    }


backend_router_v1.include_router(test_router)