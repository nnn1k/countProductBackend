from typing import Sequence

from sqlalchemy.exc import IntegrityError

from app.domains.storages.repository import StorageRepository
from app.domains.storages.schemas import (
    StorageSchema,
    StorageSchemaRel,
    StorageCreate,
)
from app.domains.users.schemas import UserSchema
from app.domains.uis.service import UserInStorageService
from app.utils.exc import (
    bad_generation_code_exc,
    user_in_storage_not_exist_exc,
    bad_storage_name_exc,
    storage_not_found_exc, user_is_not_owner_exc,
)
from app.utils.utils import get_random_code


class StorageService:
    def __init__(
        self,
        storage_repo: StorageRepository,
        uis_serv: UserInStorageService,
    ) -> None:
        self._storage_repo = storage_repo
        self._uis_serv = uis_serv

    async def create(
        self, new_storage: StorageCreate, user: UserSchema
    ) -> StorageSchema:
        code = await self._generate_unique_storage_code()
        try:
            storage = await self._storage_repo.create(
                name=new_storage.name, code=code, creator_id=user.id
            )
        except IntegrityError:
            raise bad_storage_name_exc

        await self._uis_serv.add_user(
            user_id=user.id, storage_id=storage.id, is_owner=True
        )
        return StorageSchema.model_validate(storage)

    async def get_all(
        self, user: UserSchema, rel: bool = False
    ) -> Sequence[StorageSchemaRel] | Sequence[StorageSchema]:
        return await self._uis_serv.get_all_storages_on_user(user_id=user.id, rel=rel)

    async def get_one(
        self, user: UserSchema, storage_id: int, rel: bool = False
    ) -> StorageSchema | StorageSchemaRel:
        storage = await self._uis_serv.get_one_storage_on_user(
            user=user, rel=rel, storage_id=storage_id
        )
        if not storage:
            raise user_in_storage_not_exist_exc
        return storage

    async def update(
        self, storage_id: int, new_storage: StorageCreate, user: UserSchema
    ) -> StorageSchema:
        if not await self._uis_serv.check_user_is_owner(user_id=user.id, storage_id=storage_id):
            raise user_is_not_owner_exc
        try:
            storage = await self._storage_repo.update(
                storage_id=storage_id, name=new_storage.name
            )
        except IntegrityError:
            raise bad_storage_name_exc
        if not storage:
            raise user_in_storage_not_exist_exc
        return StorageSchema.model_validate(storage)

    async def delete(self, storage_id: int, user: UserSchema) -> None:
        if not await self._uis_serv.check_user_is_owner(user_id=user.id, storage_id=storage_id):
            raise user_is_not_owner_exc
        storage = await self._storage_repo.delete(storage_id=storage_id)
        if not storage:
            raise storage_not_found_exc

    async def _generate_unique_storage_code(
        self, min_length: int = 4, max_length: int = 8, attempts: int = 5
    ) -> str:
        for length in range(min_length, max_length + 1):
            for _ in range(attempts):
                code = get_random_code(k=length)
                storage = await self._storage_repo.get_one(code=code)
                if not storage:
                    return code

        raise bad_generation_code_exc

    async def add_user_via_code(self, code: str, user: UserSchema) -> StorageSchema:
        storage = await self._storage_repo.get_one(code=code)
        if not storage:
            raise storage_not_found_exc
        await self._uis_serv.add_user(user_id=user.id, storage_id=storage.id)
        return StorageSchema.model_validate(storage)

