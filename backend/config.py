"""Configuration management for the application."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Perplexity AI Configuration
    perplexity_api_key: str
    perplexity_model: str = "sonar"
    
    # FastAPI Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # CORS Settings
    frontend_url: str = "http://localhost:5173"
    
    # Mock Service Configuration
    mock_crm_enabled: bool = True
    mock_credit_bureau_enabled: bool = True
    mock_offer_mart_enabled: bool = True
    
    # Business Rules
    min_credit_score: int = 700
    max_emi_to_salary_ratio: float = 0.5
    conditional_approval_multiplier: int = 2
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        env_file_encoding = 'utf-8'


# Global settings instance
settings = Settings()
