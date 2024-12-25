from sqlalchemy import Column, Integer, String, Float, ARRAY, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Product(Base):
    """
    SQLAlchemy model for the products table
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    short_description = Column(String)
    description = Column(Text)
    brand = Column(String, index=True)
    color = Column(String)
    price = Column(Float)
    currency = Column(String, default="USD")
    tags = Column(ARRAY(String))
    
    # Vector representation for similarity search (stored as array of floats)
    embedding = Column(ARRAY(Float))

    # Relationships
    transactions = relationship("Transaction", back_populates="product")
