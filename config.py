"""
Configuration de l'application PMS Incendie
Support des environnements multiples (dev, prod, test)
"""
import os
from typing import Optional, Any, Dict
from pydantic_settings import BaseSettings
from functools import lru_cache


class BaseConfig(BaseSettings):
    """Configuration de base commune à tous les environnements"""
    
    # Informations de l'application
    project_name: str = "PMS Protection Incendie"
    version: str = "1.0.0"
    description: str = "API de gestion de projet pour entreprise de protection incendie"
    api_v1_prefix: str = "/api/v1"
    
    # Sécurité JWT
    secret_key: str = "CHANGE-ME-IN-PRODUCTION-VERY-LONG-SECRET-KEY-HERE"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Upload de fichiers
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    
    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100
    
    # CORS (sera parsé depuis une string séparée par des virgules)
    cors_origins: str = "*"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore les variables d'environnement non définies


class DevelopmentConfig(BaseConfig):
    """Configuration pour l'environnement de développement"""
    debug: bool = True
    testing: bool = False
    
    # Base de données de développement (PostgreSQL local)
    database_url: str = "postgresql://dev_user:dev_pass123@localhost:5433/pms_incendie_dev"
    
    # CORS permissif pour le développement
    cors_origins: str = "http://localhost:3000,http://localhost:8080,http://127.0.0.1:3000,http://127.0.0.1:8080"
    
    # Uploads locaux
    upload_dir: str = "uploads/dev"
    
    # Logs détaillés
    log_level: str = "DEBUG"
    
    class Config:
        env_file = "config/.env.dev"
        case_sensitive = False
        extra = "ignore"


class ProductionConfig(BaseConfig):
    """Configuration pour l'environnement de production"""
    
    # Base de données PostgreSQL production
    database_url: str = "postgresql://prod_user:SECURE_PASSWORD@localhost:5432/pms_incendie_prod"
    
    # Configuration serveur
    host: str = "0.0.0.0"
    port: int = 80
    reload: bool = False
    
    # Sécurité renforcée
    debug: bool = False
    log_level: str = "WARNING"
    
    # CORS restreint en production
    # TODO: ajouter les origines autorisées pour le frontend
    cors_origins: str = ""
    
    # Sécurité production
    secret_key: str = "MUST-BE-CHANGED-TO-SECURE-RANDOM-STRING-IN-PRODUCTION"
    access_token_expire_minutes: int = 60
    
    # Documentation désactivée en production
    enable_docs: bool = False
    enable_redoc: bool = False
    
    class Config:
        env_file = "config/.env.prod"
        extra = "ignore"


class TestConfig(BaseConfig):
    """Configuration pour les tests"""
    
    # Base de données test en mémoire
    database_url: str = "postgresql://test_user:test_password@localhost:5434/pms_incendie_test"
    
    # Configuration test
    debug: bool = True
    log_level: str = "WARNING"
    
    # Paramètres adaptés aux tests
    access_token_expire_minutes: int = 5
    default_page_size: int = 5
    max_page_size: int = 10
    
    class Config:
        env_file = "config/.env.test"
        extra = "ignore"


# Mapping des environnements
ENVIRONMENT_CONFIGS = {
    "development": DevelopmentConfig,
    "dev": DevelopmentConfig,
    "production": ProductionConfig,
    "prod": ProductionConfig,
    "test": TestConfig,
    "testing": TestConfig,
}


def get_environment() -> str:
    """
    Détermine l'environnement actuel basé sur la variable ENVIRONMENT
    Par défaut: development
    """
    return os.getenv("ENVIRONMENT", "development").lower()


@lru_cache()
def get_settings() -> BaseConfig:
    """
    Factory pattern pour obtenir la configuration selon l'environnement
    Utilise le cache pour éviter de recréer la config à chaque appel
    """
    environment = get_environment()
    
    config_class = ENVIRONMENT_CONFIGS.get(environment)
    if not config_class:
        available = ", ".join(ENVIRONMENT_CONFIGS.keys())
        raise ValueError(f"Environment '{environment}' not supported. Available: {available}")
    
    print(f"🔧 Loading {environment} configuration...")
    return config_class()


# Instance globale des paramètres (se configure automatiquement)
settings = get_settings()


# Fonction utilitaire pour réinitialiser la config (utile pour les tests)
def reload_settings():
    """Force le rechargement de la configuration"""
    get_settings.cache_clear()
    global settings
    settings = get_settings()
    return settings


# Fonction utilitaire pour convertir CORS en liste
def get_cors_origins_list():
    """Convertit la chaîne CORS en liste"""
    if settings.cors_origins == "*":
        return ["*"]
    return [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]


# Fonction pour obtenir des infos sur l'environnement actuel

def get_environment_info() -> Dict[str, Any]:
    """Retourne des informations sur l'environnement actuel"""
    env = get_environment()
    return {
        "environment": env,
        "config_class": settings.__class__.__name__,
        "database_host": settings.database_url.split("@")[1].split("/")[0] if "@" in settings.database_url else "unknown",
        "debug_mode": settings.debug,
        "docs_enabled": getattr(settings, 'enable_docs', True),
        "port": getattr(settings, 'port', 8000),
        "log_level": settings.log_level
    } 