"""
Dépendances communes pour l'API
"""
from typing import Optional
from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from schemas.common import PaginationParams, FilterParams
from config import settings


def get_pagination_params(
    page: int = Query(1, ge=1, description="Numéro de page"),
    page_size: int = Query(settings.default_page_size, ge=1, le=settings.max_page_size, description="Taille de page")
) -> PaginationParams:
    """Dépendance pour les paramètres de pagination"""
    return PaginationParams(page=page, page_size=page_size)


def get_filter_params(
    q: Optional[str] = Query(None, description="Recherche textuelle"),
    date_from: Optional[str] = Query(None, description="Date de début (ISO format)"),
    date_to: Optional[str] = Query(None, description="Date de fin (ISO format)")
) -> FilterParams:
    """Dépendance pour les paramètres de filtrage"""
    return FilterParams(q=q, date_from=date_from, date_to=date_to)


def require_authenticated_user(current_user=Depends(get_current_user)):
    """Dépendance pour exiger un utilisateur authentifié"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return current_user


def require_admin_user(current_user=Depends(get_current_user)):
    """Dépendance pour exiger un utilisateur admin"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    # TODO: Vérifier le rôle admin
    # Pour l'instant, on accepte tous les utilisateurs authentifiés
    return current_user


def get_current_user_id(current_user=Depends(get_current_user)) -> int:
    """Récupère l'ID de l'utilisateur courant"""
    return current_user["id"]


class CommonQueryParams:
    """Classe pour les paramètres de requête communs"""
    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
        limit: int = Query(100, ge=1, le=1000, description="Nombre max d'éléments"),
        q: Optional[str] = Query(None, description="Recherche textuelle")
    ):
        self.skip = skip
        self.limit = limit
        self.q = q 