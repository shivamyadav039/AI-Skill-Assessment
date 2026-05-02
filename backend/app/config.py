"""
Configuration settings for the backend application.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App Config
    APP_NAME: str = "AI Skill Assessment Agent"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Server Config
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    
    # Database Config
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/skill_assessment"
    DB_ECHO: bool = False  # Log SQL queries
    
    # AI/LLM Config (NVIDIA NIM)
    NVIDIA_API_KEY: Optional[str] = None
    LLM_MODEL: str = "nvidia/llama-3.3-nemotron-super-49b-v1"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2048
    
    # NLP Config
    SPACY_MODEL: str = "en_core_web_sm"
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"
    
    # Assessment Config
    MAX_TURNS_PER_SKILL: int = 5
    SKILL_ASSESSMENT_TIMEOUT_SECONDS: int = 3600  # 1 hour
    
    # RAG Config
    RAG_ENABLED: bool = True
    COURSE_DATABASE_URL: Optional[str] = None
    
    # CORS Config
    CORS_ORIGINS: list = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }


settings = Settings()
