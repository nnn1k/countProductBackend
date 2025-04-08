
from pydantic import BaseModel, ConfigDict

from backend.src.lib.classes.enum_classes.unitenum import UnitEnum


class ProductSchema(BaseModel):
    id: int
    name: str
    category_id: int
    unit: UnitEnum
    storage_id: int
    quantity: float
    recommended: float
    created_at: int
    updated_at: int

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    name: str
    unit: UnitEnum
    quantity: float
    recommended: float
