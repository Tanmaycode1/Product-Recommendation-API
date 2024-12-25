from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Customer(Base):
    """
    SQLAlchemy model for the customers table
    """
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(Enum(Gender))
    city = Column(String)
    country = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)

    # Relationships
    transactions = relationship("Transaction", back_populates="customer")
