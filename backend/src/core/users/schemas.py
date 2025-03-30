from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    id: int
    nickname: str
    email: str
    created_at: int
    updated_at: int

    model_config = ConfigDict(from_attributes=True)


class UserSchemaRel(UserSchema):
    storages: Optional[List['StorageSchema']] = []
