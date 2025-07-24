import datetime
from typing import List, Optional, Sequence

from pydantic import BaseModel, ConfigDict


class StorageSchema(BaseModel):
    id: int
    name: str
    code: str
    creator_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class StorageSchemaRel(StorageSchema):
    users: Optional[List['UserSchema']] = []
    categories: Optional[List['CategorySchema']] = []


class StorageCreate(BaseModel):
    name: str


class StorageSchemaResponse(BaseModel):
    storage: StorageSchema


class StoragesSchemaResponse(BaseModel):
    storages: Sequence[StorageSchema]


class StorageSchemaRelResponse(BaseModel):
    storage: StorageSchemaRel
