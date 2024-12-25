# app/utils/data_generator.py
from faker import Faker
from app.db.base import SessionLocal
from app.models.customer import Customer, Gender
from app.models.product import Product
from app.models.transaction import Transaction
import random
from datetime import datetime, timedelta
from typing import List
from sentence_transformers import SentenceTransformer

fake = Faker()

# Categories and their associated tags
PRODUCT_CATEGORIES = {
    "t-shirt": ["casual", "summer", "cotton", "comfortable"],
    "trousers": ["formal", "casual", "denim", "cotton"],
    "dress": ["formal", "party", "elegant", "summer"],
    "jacket": ["winter", "outdoor", "casual", "warm"],
    "shoes": ["comfortable", "casual", "formal", "sports"]
}

# Brands and their typical price ranges
BRANDS = {
    "Zara": (29.99, 199.99),
    "H&M": (19.99, 99.99),
    "Nike": (39.99, 199.99),
    "Adidas": (34.99, 179.99),
    "Mango": (25.99, 149.99),
    "Uniqlo": (14.99, 89.99),
    "Puma": (29.99, 159.99),
    "Levi's": (39.99, 199.99),
    "Zudio": (9.99, 49.99)
}

COLORS = ["Black", "White", "Red", "Blue", "Green", "Yellow", "Pink", "Gray", "Navy", "Brown"]

class DataGenerator:
    """
    Utility class for generating sample data for the product recommendation system
    """
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.db = SessionLocal()

    def generate_customers(self, num_customers: int) -> List[Customer]:
        """
        Generate sample customer data
        
        Args:
            num_customers: Number of customers to generate
            
        Returns:
            List of generated Customer objects
        """
        customers = []
        for _ in range(num_customers):
            customer = Customer(
                name=fake.name(),
                age=random.randint(18, 70),
                gender=random.choice(list(Gender)),
                city=fake.city(),
                country=fake.country(),
                email=fake.email(),
                phone=fake.phone_number()
            )
            customers.append(customer)
        
        self.db.add_all(customers)
        self.db.commit()
        return customers

    def generate_product_description(self, category: str, brand: str) -> tuple:
        """
        Generate product descriptions based on category and brand
        
        Args:
            category: Product category
            brand: Product brand
            
        Returns:
            Tuple of (short_description, long_description)
        """
        adjectives = ["Stylish", "Modern", "Comfortable", "Trendy", "Classic", "Elegant"]
        materials = ["Cotton", "Polyester", "Denim", "Wool", "Linen"]
        
        short_desc = f"{random.choice(adjectives)} {category} by {brand}"
        
        long_desc = f"This {random.choice(adjectives).lower()} {category} from {brand} " \
                   f"is made from high-quality {random.choice(materials).lower()}. " \
                   f"Perfect for {random.choice(['casual', 'formal', 'everyday'])} wear. " \
                   f"{random.choice(['Featuring a modern design', 'With classic styling', 'In a timeless style'])}, " \
                   f"this piece {random.choice(['will complement any wardrobe', 'is a must-have this season', 'offers both style and comfort'])}."
        
        return short_desc, long_desc

    def generate_products(self, num_products: int) -> List[Product]:
        """
        Generate sample product data
        
        Args:
            num_products: Number of products to generate
            
        Returns:
            List of generated Product objects
        """
        products = []
        for _ in range(num_products):
            category = random.choice(list(PRODUCT_CATEGORIES.keys()))
            brand = random.choice(list(BRANDS.keys()))
            price_range = BRANDS[brand]
            
            short_desc, long_desc = self.generate_product_description(category, brand)
            
            # Generate base tags from category
            tags = PRODUCT_CATEGORIES[category].copy()
            # Add random additional tags
            tags.extend(random.sample(["trending", "bestseller", "new", "limited", "sale"], 
                                   random.randint(1, 3)))
            
            # Create product text for embedding
            product_text = f"{category} {brand} {short_desc} {long_desc} {' '.join(tags)}"
            embedding = self.model.encode([product_text])[0].tolist()
            
            product = Product(
                name=f"{brand} {category.title()} {random.randint(1000, 9999)}",
                category=category,
                short_description=short_desc,
                description=long_desc,
                brand=brand,
                color=random.choice(COLORS),
                price=round(random.uniform(price_range[0], price_range[1]), 2),
                currency="USD",
                tags=tags,
                embedding=embedding
            )
            products.append(product)
        
        self.db.add_all(products)
        self.db.commit()
        return products

    def generate_transactions(self, num_transactions: int) -> List[Transaction]:
        """
        Generate sample transaction data
        
        Args:
            num_transactions: Number of transactions to generate
            
        Returns:
            List of generated Transaction objects
        """
        customers = self.db.query(Customer).all()
        products = self.db.query(Product).all()
        
        transactions = []
        start_date = datetime.now() - timedelta(days=365)
        
        for _ in range(num_transactions):
            product = random.choice(products)
            customer = random.choice(customers)
            
            # 10% chance of return
            is_returned = random.random() < 0.1
            
            # Generate rating and review for non-returned items
            if not is_returned and random.random() < 0.7:  # 70% chance of rating
                rating = random.uniform(3.0, 5.0)  # Bias towards positive ratings
                review_text = fake.paragraph()
            else:
                rating = None
                review_text = None
            
            transaction = Transaction(
                product_id=product.id,
                customer_id=customer.id,
                amount_paid=product.price,
                purchase_date=fake.date_time_between(start_date=start_date),
                is_returned=is_returned,
                rating=rating,
                review_text=review_text
            )
            transactions.append(transaction)
        
        self.db.add_all(transactions)
        self.db.commit()
        return transactions

    def generate_sample_data(self):
        """
        Generate complete sample dataset
        """
        print("Generating customers...")
        self.generate_customers(100)
        
        print("Generating products...")
        self.generate_products(200)
        
        print("Generating transactions...")
        self.generate_transactions(500)
        
        print("Sample data generation complete!")


if __name__ == "__main__":
    generator = DataGenerator()
    generator.generate_sample_data()