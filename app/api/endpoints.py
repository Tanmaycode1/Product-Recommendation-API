# app/api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.base import get_db
from app.schemas.product import ProductSearch, ProductInDB, ProductRecommendation
from app.schemas.customer import CustomerInDB
from app.schemas.transaction import TransactionInDB
from app.services.recommendation import RecommendationService
from app.services.search import SearchService
from app.models.product import Product
from app.models.customer import Customer
from app.models.transaction import Transaction

router = APIRouter()

# Initialize services
recommendation_service = RecommendationService()
search_service = SearchService()

@router.get("/search/", response_model=List[ProductInDB])
async def search_products(
    query: str = Query(..., min_length=1),
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """
    Search for products with optional filters
    """
    products = search_service.search_products(
        db=db,
        query=query,
        category=category,
        brand=brand,
        min_price=min_price,
        max_price=max_price
    )
    return products

@router.get("/recommendations/similar/", response_model=List[ProductRecommendation])
async def get_similar_products(
    query: str = Query(..., min_length=1),
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """
    Get product recommendations based on text similarity
    """
    similar_products = recommendation_service.search_similar_products(
        db=db,
        query=query,
        category=category,
        brand=brand,
        min_price=min_price,
        max_price=max_price
    )
    return [
        ProductRecommendation(product=product, similarity_score=score)
        for product, score in similar_products
    ]

@router.get("/recommendations/collaborative/{customer_id}", response_model=List[ProductInDB])
async def get_collaborative_recommendations(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """
    Get product recommendations based on collaborative filtering
    """
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
        
    recommendations = recommendation_service.get_collaborative_recommendations(
        db=db,
        customer_id=customer_id
    )
    return recommendations

@router.get("/products/", response_model=List[ProductInDB])
async def get_all_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all products with pagination
    """
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.get("/products/{product_id}", response_model=ProductInDB)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific product by ID
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/customers/", response_model=List[CustomerInDB])
async def get_all_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all customers with pagination
    """
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers

@router.get("/transactions/", response_model=List[TransactionInDB])
async def get_all_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all transactions with pagination
    """
    transactions = db.query(Transaction).offset(skip).limit(limit).all()
    return transactions

@router.get("/transactions/customer/{customer_id}", response_model=List[TransactionInDB])
async def get_customer_transactions(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all transactions for a specific customer
    """
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
        
    transactions = db.query(Transaction).filter(
        Transaction.customer_id == customer_id
    ).all()
    return transactions