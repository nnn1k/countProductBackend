import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, ConfigDict


class UserSchema(BaseModel):
    id: int
    nickname: str
    email: EmailStr
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class UserSchemaRel(UserSchema):
    storages: Optional[List['StorageSchema']] = []


class UserSchemaResponse(BaseModel):
    user: UserSchema


class UserSchemaRelResponse(BaseModel):
    user: UserSchemaRel
