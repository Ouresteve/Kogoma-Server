from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    image_url: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    image_url: Optional[str]

class ProductOut(BaseModel):
    id: str
    name: str
    description: str
    price: float
    image_url: Optional[str]
