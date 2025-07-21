"""
Schémas Pydantic communs
"""
from typing import Optional, Generic, TypeVar, List
from datetime import datetime
from pydantic import BaseModel, Field

T = TypeVar('T')


class PaginationParams(BaseModel):
    """Paramètres de pagination"""
    page: int = Field(1, ge=1, description="Numéro de page")
    page_size: int = Field(20, ge=1, le=100, description="Taille de page")


class PaginatedResponse(BaseModel, Generic[T]):
    """Réponse paginée générique"""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int


class FilterParams(BaseModel):
    """Paramètres de filtrage communs"""
    q: Optional[str] = Field(None, description="Recherche textuelle")
    date_from: Optional[datetime] = Field(None, description="Date de début")
    date_to: Optional[datetime] = Field(None, description="Date de fin")


class BaseSchema(BaseModel):
    """Schéma de base avec configuration commune"""
    class Config:
        from_attributes = True  # Pour SQLAlchemy v2
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class TimestampMixin(BaseModel):
    """Mixin pour les timestamps"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ResponseMessage(BaseModel):
    """Message de réponse simple"""
    message: str
    success: bool = True 