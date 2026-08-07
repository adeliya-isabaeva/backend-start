# schemas.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class ItemCreate(BaseModel):
    name: str
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    description: Optional[str] = None

class ItemOut(BaseModel):
    id: int
    name: str
    price: float
    stock_quantity: int
    description: Optional[str] = None

    # Это позволяет Pydantic брать поля из SQLAlchemy-объекта (работает и для SQLite, и для Postgres)
    model_config = ConfigDict(from_attributes=True)
