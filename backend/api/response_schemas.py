from typing import Sequence

from pydantic import BaseModel

from backend.src.core.categories.schemas import CategorySchema
from backend.src.core.storages.schemas import StorageSchema, StorageSchemaRel
from backend.src.core.users.schemas import UserSchema, UserSchemaRel


class UserSchemaResponse(BaseModel):
    user: UserSchema


class UserSchemaRelResponse(BaseModel):
    user: UserSchemaRel


class StorageSchemaResponse(BaseModel):
    storage: StorageSchema


class StoragesSchemaResponse(BaseModel):
    storages: Sequence[StorageSchema]


class StorageSchemaRelResponse(BaseModel):
    storage: StorageSchemaRel


class CategorySchemaResponse(BaseModel):
    category: CategorySchema


class CategoriesSchemaResponse(BaseModel):
    categories: Sequence[CategorySchema]
