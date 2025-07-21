"""
Modèles de base pour SQLAlchemy
"""
from datetime import datetime
from sqlalchemy import Column, BigInteger, DateTime, func
from database import Base


class TimestampMixin:
    """Mixin pour ajouter created_at et updated_at aux modèles"""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class BaseModel(Base, TimestampMixin):
    """Classe de base abstraite pour tous les modèles"""
    __abstract__ = True
    
    id = Column(BigInteger, primary_key=True, autoincrement=True) 