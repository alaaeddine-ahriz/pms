"""
Configuration de l'application PMS Incendie
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Base de données PostgreSQL
    database_url: str = "postgresql://user:password@localhost:5432/pms_incendie"
    
    # JWT
    secret_key: str = "votre-cle-secrete-super-longue-et-complexe-a-changer"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # API
    api_v1_prefix: str = "/api/v1"
    project_name: str = "PMS Protection Incendie"
    version: str = "1.0.0"
    description: str = "API de gestion de projet pour entreprise de protection incendie"
    
    # Upload de fichiers
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    
    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100
    
    # Debug
    debug: bool = False
    
    class Config:
        env_file = ".env"


# Instance globale des paramètres
settings = Settings() 