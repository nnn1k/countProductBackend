from typing import Sequence

from sqlalchemy.exc import IntegrityError

from backend.src.core.users.schemas import UserSchema
from backend.src.core.storages.schemas import StorageSchemaRel, StorageSchema
from backend.src.core.uis.repository import UserInStorageRepository
from backend.src.lib.exc import (
    user_in_storage_exist_exc,
    user_in_storage_not_exist_exc, user_is_not_owner_exc,
)


class UserInStorageService:

    def __init__(self, uis_repo: UserInStorageRepository) -> None:
        self.uis_repo = uis_repo

    async def add_user(self, user_id: int, storage_id: int, is_owner: bool = False) -> None:
        try:
            await self.uis_repo.add_user_in_storage(user_id, storage_id, is_owner)
        except IntegrityError:
            raise user_in_storage_exist_exc

    async def get_all_storages_on_user(
            self,
            user_id: int,
            rel: bool = False
    ) -> Sequence[StorageSchemaRel] | Sequence[StorageSchema]:
        storages = await self.uis_repo.get_all_storages_on_user(user_id=user_id, rel=rel)
        if rel:
            return [StorageSchemaRel.model_validate(storage) for storage in storages]
        return [StorageSchema.model_validate(storage) for storage in storages]

    async def get_one_storage_on_user(
            self,
            user: UserSchema,
            storage_id: int,
            rel: bool = False
    ) -> StorageSchemaRel | StorageSchema:
        storage = await self.uis_repo.get_one_storage_on_user(user.id, storage_id)
        if rel:
            return StorageSchemaRel.model_validate(storage)
        return StorageSchema.model_validate(storage)

    async def delete_user(self, user: UserSchema, user_id: int, storage_id: int) -> None:
        await self.check_user_is_owner(storage_id=storage_id, user_id=user.id)
        result = await self.uis_repo.delete_user(user_id=user_id, storage_id=storage_id)
        if not result:
            raise user_in_storage_not_exist_exc

    async def check_user_is_owner(self, storage_id: int, user_id: int) -> None:
        if not await self.uis_repo.check_user_in_storage(storage_id=storage_id, user_id=user_id, is_owner=True):
            raise user_is_not_owner_exc

    async def check_user_in_storage(self, storage_id: int, user_id: int) -> None:
        if not await self.uis_repo.check_user_in_storage(storage_id=storage_id, user_id=user_id):
            raise user_in_storage_not_exist_exc

