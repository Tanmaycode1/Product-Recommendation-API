from sqlalchemy import Column, Integer, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Transaction(Base):
    """
    SQLAlchemy model for the transactions table
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    amount_paid = Column(Float)
    purchase_date = Column(DateTime, default=datetime.utcnow)
    is_returned = Column(Boolean, default=False)
    rating = Column(Float)
    review_text = Column(Text)

    # Relationships
    product = relationship("Product", back_populates="transactions")
    customer = relationship("Customer", back_populates="transactions")