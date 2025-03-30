from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class StorageSchema(BaseModel):
    id: int
    name: str
    code: str
    creator_id: int
    created_at: int
    updated_at: int

    model_config = ConfigDict(from_attributes=True)


class StorageSchemaRel(StorageSchema):
    users: Optional[List['UserSchema']] = []


class StorageCreate(BaseModel):
    name: str
