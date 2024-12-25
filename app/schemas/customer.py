from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.customer import Gender

class CustomerBase(BaseModel):
    name: str
    age: int
    gender: Gender
    city: str
    country: str
    email: EmailStr
    phone: str

class CustomerCreate(CustomerBase):
    pass

class CustomerInDB(CustomerBase):
    id: int

    class Config:
        from_attributes = True