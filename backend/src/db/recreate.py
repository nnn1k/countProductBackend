from backend.src.db.base import Base
from backend.src.db.core import engine

from backend.src.db.models.users import UserOrm
from backend.src.db.models.storages import StorageOrm
from backend.src.db.models.users_in_storages import UserInStorageOrm
from backend.src.db.models.products import ProductOrm
from backend.src.db.models.categories import CategoryOrm, SystemCategoryOrm


async def recreate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
