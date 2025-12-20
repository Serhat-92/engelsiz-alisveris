from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Engelsiz Alışveriş API"
    API_V1_STR: str = "/api/v1"
    
    # Güvenlik: Bu anahtarı üretim ortamında mutlaka değiştirin! (.env dosyasından okumalı)
    SECRET_KEY: str = "super-secret-key-for-dev-environment-only-change-in-prod" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS (Cross-Origin Resource Sharing)
    BACKEND_CORS_ORIGINS: List[str] = ["*"] # Mobile app için genelde * veya spesifik domain

    class Config:
        case_sensitive = True

settings = Settings()
