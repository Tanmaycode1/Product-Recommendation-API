# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional, List
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    """
    Application settings. These values are loaded from environment variables.
    """
    # Project name
    PROJECT_NAME: str = "Product Recommendation API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # PostgreSQL database configuration
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "product_recommendation"
    POSTGRES_PORT: str = "5432"
    
    # Recommendation system settings
    SIMILARITY_THRESHOLD: float = 0.3
    TOP_N_RECOMMENDATIONS: int = 5
    
    # JWT token configuration
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Additional settings that were missing
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:8080", "http://localhost:3000"]
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Performance settings
    MAX_CONNECTIONS: int = 100
    POOL_SIZE: int = 20
    POOL_TIMEOUT: int = 30
    
    # Search settings
    MIN_SEARCH_CHARS: int = 3
    MAX_SEARCH_RESULTS: int = 50
    FUZZY_MATCH_THRESHOLD: float = 0.6
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """
        Constructs and returns the PostgreSQL database URI
        """
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()