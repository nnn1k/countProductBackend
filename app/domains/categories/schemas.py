import datetime
from typing import Optional, Sequence

from pydantic import BaseModel, ConfigDict


class CategorySchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = ''
    storage_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = ''


class CategorySchemaResponse(BaseModel):
    category: CategorySchema


class CategoriesSchemaResponse(BaseModel):
    categories: Sequence[CategorySchema]
