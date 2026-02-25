"""
Application configuration using Pydantic Settings.
Environment variables override default values.
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "Human Nutrition AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8001
    
    # CORS
    CORS_ORIGINS: str = "*"
    
    # RAG Settings
    PDF_PATH: str = "data/HumanNutrition.pdf"
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150
    RETRIEVER_K: int = 3
    
    # LLM Settings  
    LLM_MODEL: str = "llama3.1"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Paths
    STATIC_DIR: str = "static"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to avoid re-reading environment on every request.
    """
    return Settings()


# Convenience export
settings = get_settings()
