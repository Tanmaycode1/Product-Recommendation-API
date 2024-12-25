from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    product_id: int
    customer_id: int
    amount_paid: float
    is_returned: bool = False
    rating: Optional[float] = None
    review_text: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionInDB(TransactionBase):
    id: int
    purchase_date: datetime

    class Config:
        from_attributes = True