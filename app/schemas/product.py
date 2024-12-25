from pydantic import BaseModel
from typing import List, Optional

class ProductBase(BaseModel):
    name: str
    category: str
    short_description: str
    description: str
    brand: str
    color: str
    price: float
    currency: str = "USD"
    tags: List[str]

class ProductCreate(ProductBase):
    pass

class ProductInDB(ProductBase):
    id: int

    class Config:
        from_attributes = True

class ProductSearch(BaseModel):
    query: str
    category: Optional[str] = None
    brand: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None

class ProductRecommendation(BaseModel):
    product: ProductInDB
    similarity_score: float
