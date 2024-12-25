# app/db/init_db.py
from sqlalchemy import create_engine
from app.core.config import settings
from app.db.base import Base
from app.models.customer import Customer
from app.models.product import Product
from app.models.transaction import Transaction

def init_db():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Tables created successfully!")