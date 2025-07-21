"""
Configuration de la base de données PostgreSQL
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from config import settings

# Création du moteur SQLAlchemy
engine = create_engine(settings.database_url)

# Factory de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modèles ORM
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dépendance pour obtenir une session de base de données
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Crée toutes les tables en base de données
    """
    Base.metadata.create_all(bind=engine) 