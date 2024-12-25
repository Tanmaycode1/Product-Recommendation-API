# app/services/recommendation.py
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sqlalchemy.orm import Session
from typing import List, Tuple
from app.models.product import Product
from app.models.transaction import Transaction  # Add this import
from app.core.config import settings
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

class RecommendationService:
    """
    Service for handling product recommendations using sentence transformers
    and cosine similarity
    """
    def __init__(self):
        """Initialize the recommendation service with the BERT model"""
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text by tokenizing and removing stop words
        
        Args:
            text: Input text to preprocess
            
        Returns:
            Preprocessed text string
        """
        tokens = word_tokenize(text.lower())
        tokens = [t for t in tokens if t not in self.stop_words]
        return ' '.join(tokens)

    def get_text_embedding(self, text: str) -> np.ndarray:
        """
        Get embedding vector for input text
        
        Args:
            text: Input text to embed
            
        Returns:
            Numpy array containing text embedding
        """
        preprocessed_text = self.preprocess_text(text)
        return self.model.encode([preprocessed_text])[0]

    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score
        """
        return cosine_similarity(
            embedding1.reshape(1, -1), 
            embedding2.reshape(1, -1)
        )[0][0]

    def get_collaborative_recommendations(
        self, 
        db: Session, 
        customer_id: int
    ) -> List[Product]:
        """
        Get product recommendations based on collaborative filtering
        
        Args:
            db: Database session
            customer_id: ID of the customer to get recommendations for
            
        Returns:
            List of recommended products
        """
        # Get customer's previous purchases
        customer_products = (
            db.query(Product)
            .join(Transaction)
            .filter(Transaction.customer_id == customer_id)
            .all()
        )
        
        if not customer_products:
            return []

        # Get common tags from customer's purchases
        customer_tags = set()
        for product in customer_products:
            customer_tags.update(product.tags)
        
        # Find products with similar tags that the customer hasn't bought
        similar_products = (
            db.query(Product)
            .filter(Product.id.notin_([p.id for p in customer_products]))
            .all()
        )
        
        # Score products based on tag overlap
        scored_products = []
        for product in similar_products:
            product_tags = set(product.tags)
            tag_overlap = len(customer_tags.intersection(product_tags))
            if tag_overlap > 0:
                scored_products.append((product, tag_overlap))
        
        # Sort by score and return top recommendations
        scored_products.sort(key=lambda x: x[1], reverse=True)
        return [p[0] for p in scored_products[:settings.TOP_N_RECOMMENDATIONS]]

    def search_similar_products(
        self, 
        db: Session, 
        query: str,
        category: str = None,
        brand: str = None,
        min_price: float = None,
        max_price: float = None
    ) -> List[Tuple[Product, float]]:
        """
        Search for products similar to the query text
        
        Args:
            db: Database session
            query: Search query text
            category: Optional category filter
            brand: Optional brand filter
            min_price: Optional minimum price filter
            max_price: Optional maximum price filter
            
        Returns:
            List of tuples containing (product, similarity_score)
        """
        # Get query embedding
        query_embedding = self.get_text_embedding(query)
        
        # Build base query
        products_query = db.query(Product)
        
        # Apply filters
        if category:
            products_query = products_query.filter(Product.category == category)
        if brand:
            products_query = products_query.filter(Product.brand == brand)
        if min_price is not None:
            products_query = products_query.filter(Product.price >= min_price)
        if max_price is not None:
            products_query = products_query.filter(Product.price <= max_price)
        
        # Get all products
        products = products_query.all()
        
        # Calculate similarities
        similarities = []
        for product in products:
            product_text = f"{product.name} {product.description} {' '.join(product.tags)}"
            product_embedding = self.get_text_embedding(product_text)
            similarity = self.calculate_similarity(query_embedding, product_embedding)
            
            if similarity >= settings.SIMILARITY_THRESHOLD:
                similarities.append((product, similarity))
        
        # Sort by similarity score
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:settings.TOP_N_RECOMMENDATIONS]