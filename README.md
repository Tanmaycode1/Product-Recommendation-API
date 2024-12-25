# Product Recommendation System API

A FastAPI-powered product recommendation system with PostgreSQL backend. The system provides text-based search functionality and generates product recommendations using both content-based (text similarity) and collaborative filtering approaches.

<img width="1470" alt="image" src="https://github.com/user-attachments/assets/44b04849-c5d5-47e0-bc7d-75bfdfcef78a" />


## Tech Stack
- **Programming Language**: Python
- **Frameworks**: FastAPI/Flask/Django (depending on your implementation)
- **Database**: PostgreSQL/MySQL
- **Libraries**:
  - **Sentence Transformers**: For generating embeddings from textual data.
  - **Scikit-learn**: For calculating cosine similarity.
  - **NLTK**: For tokenizing and cleaning text data.
  - **Levenshtein**: For fuzzy string matching in search.
  - **SQLAlchemy**: For database ORM.
- **Other Tools**:
  - **Docker**: For containerized deployments (if applicable).
  - **Cloud Storage**: (Optional, for scalable deployments)

---

## How It Works

### Recommendation Service

The **Recommendation Service** combines collaborative filtering with semantic similarity using pre-trained text embeddings. 

1. **Collaborative Filtering**:
   - Identifies products purchased by a customer.
   - Recommends similar products based on shared tags or attributes.
   
2. **Semantic Similarity**:
   - Preprocesses product descriptions and user inputs.
   - Converts texts into vector embeddings using a pre-trained model (`paraphrase-MiniLM-L6-v2`).
   - Measures cosine similarity between product vectors and user preferences.
   - Filters and ranks products based on similarity scores.

#### Example Flow:
- Input: User Query (e.g., "Wireless headphones")
- Output: Top N recommendations based on matching product descriptions, tags, and categories.

---

### Search Service

The **Search Service** allows users to search for products using flexible filters and fuzzy matching. 

1. **Fuzzy Matching**:
   - Compares the user's search term with product names, descriptions, tags, and brands.
   - Computes similarity scores using the Levenshtein distance.

2. **Search Filtering**:
   - Filters results by product attributes such as category, brand, and price range.

3. **Sorting and Ranking**:
   - Results are sorted based on fuzzy matching scores and presented to the user.

#### Example Flow:
- Input: Search Term (e.g., "Bluetooth earbuds"), Filters (e.g., Category: "Electronics", Price: "< 3000")
- Output: Sorted product list matching the query and filters.

---

Let me know if you’d like additional refinements!
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

