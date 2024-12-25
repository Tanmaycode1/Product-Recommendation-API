from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from app.models.product import Product
from Levenshtein import ratio

class SearchService:
    """
    Service for handling product search functionality with fuzzy matching
    """
    def __init__(self):
        self.min_similarity = 0.6  # Minimum Levenshtein ratio for fuzzy matching

    def fuzzy_search(self, search_term: str, text: str) -> float:
        """
        Perform fuzzy string matching using Levenshtein distance
        
        Args:
            search_term: Search query term
            text: Text to match against
            
        Returns:
            Similarity ratio between 0 and 1
        """
        return ratio(search_term.lower(), text.lower())

    def search_products(
        self,
        db: Session,
        query: str,
        category: str = None,
        brand: str = None,
        min_price: float = None,
        max_price: float = None
    ) -> List[Product]:
        """
        Search for products using fuzzy matching and filters
        
        Args:
            db: Database session
            query: Search query text
            category: Optional category filter
            brand: Optional brand filter
            min_price: Optional minimum price filter
            max_price: Optional maximum price filter
            
        Returns:
            List of matching products
        """
        # Start with base query
        products = db.query(Product)
        
        # Apply filters if provided
        if category:
            products = products.filter(Product.category == category)
        if brand:
            products = products.filter(Product.brand == brand)
        if min_price is not None:
            products = products.filter(Product.price >= min_price)
        if max_price is not None:
            products = products.filter(Product.price <= max_price)
        
        # Get all products that might match
        all_products = products.all()
        
        # Perform fuzzy matching on product names and descriptions
        matched_products = []
        search_terms = query.split()
        
        for product in all_products:
            # Check each search term against product fields
            max_similarity = 0
            for term in search_terms:
                # Check similarity with name
                name_similarity = self.fuzzy_search(term, product.name)
                max_similarity = max(max_similarity, name_similarity)
                
                # Check similarity with description
                desc_similarity = self.fuzzy_search(term, product.short_description)
                max_similarity = max(max_similarity, desc_similarity)
                
                # Check similarity with brand
                brand_similarity = self.fuzzy_search(term, product.brand)
                max_similarity = max(max_similarity, brand_similarity)
                
                # Check similarity with tags
                for tag in product.tags:
                    tag_similarity = self.fuzzy_search(term, tag)
                    max_similarity = max(max_similarity, tag_similarity)
            
            if max_similarity >= self.min_similarity:
                matched_products.append((product, max_similarity))
        
        # Sort by similarity score
        matched_products.sort(key=lambda x: x[1], reverse=True)
        
        # Return only the products, without scores
        return [p[0] for p in matched_products]
