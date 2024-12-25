# Product Recommendation System API

A FastAPI-powered product recommendation system with PostgreSQL backend. The system provides text-based search functionality and generates product recommendations using both content-based (text similarity) and collaborative filtering approaches.

## Features

- Text-based product search with fuzzy matching
- Content-based recommendations using sentence transformers
- Collaborative filtering based on user purchase history
- Complete CRUD operations for products, customers, and transactions
- Sample data generation utility
- Detailed API documentation with OpenAPI/Swagger UI

## Requirements

- Python (3.8 - 3.11)
- Note: Python 3.12 is not yet fully supported by all dependencies
- PostgreSQL 12+
- Poetry (recommended) or pip

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/product-recommendation-system.git
cd product-recommendation-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL:
   - Create a new PostgreSQL database
   - Update the database connection settings in `.env` file (use `.env.example` as template)

5. Generate sample data:
```bash
python -m app.utils.data_generator
```

## Usage

1. Start the API server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Search and Recommendations
- `GET /api/v1/search/`: Search products with optional filters
- `GET /api/v1/recommendations/similar/`: Get similar products based on text similarity
- `GET /api/v1/recommendations/collaborative/{customer_id}`: Get recommendations based on purchase history

### Products
- `GET /api/v1/products/`: List all products
- `GET /api/v1/products/{product_id}`: Get specific product

### Customers
- `GET /api/v1/customers/`: List all customers

### Transactions
- `GET /api/v1/transactions/`: List all transactions
- `GET /api/v1/transactions/customer/{customer_id}`: Get customer's transactions

## Project Structure

```
product_recommendation_system/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── base.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── customer.py
│   │   ├── product.py
│   │   └── transaction.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── customer.py
│   │   ├── product.py
│   │   └── transaction.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── recommendation.py
│   │   └── search.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── data_generator.py
│   ├── __init__.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
POSTGRES_SERVER=localhost
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=product_recommendation
POSTGRES_PORT=5432
```

