from pydantic import BaseModel, Field
from typing import Optional

class ItemOut(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None

class Item(BaseModel):
    name: str
    price: float = Field(gt=0)
    description: Optional[str] = None