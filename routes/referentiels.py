"""
Routes pour les données de référence
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_pagination_params, require_authenticated_user
from schemas.common import PaginationParams, PaginatedResponse, ResponseMessage
from schemas.referentiels import *
from models.referentiels import *

router = APIRouter(prefix="/api/v1", tags=["Reference Data"])


# ======================= DEVISES ==========================

@router.get("/devise", response_model=List[DeviseResponse])
async def list_devises(
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des devises ISO-4217"""
    devises = db.query(Devise).all()
    return devises


@router.post("/devise", response_model=DeviseResponse, status_code=status.HTTP_201_CREATED)
async def create_devise(
    devise_data: DeviseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer une nouvelle devise"""
    # Vérifier si la devise existe déjà
    existing = db.query(Devise).filter(Devise.code == devise_data.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Currency {devise_data.code} already exists"
        )
    
    devise = Devise(**devise_data.model_dump())
    db.add(devise)
    db.commit()
    db.refresh(devise)
    return devise


# ======================= CATÉGORIES DE DÉPENSES ==========================

@router.get("/expense-categories", response_model=List[ExpenseCategoryResponse])
async def list_expense_categories(
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des catégories de dépenses"""
    categories = db.query(ExpenseCategory).all()
    return categories


@router.post("/expense-categories", response_model=ExpenseCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_expense_category(
    category_data: ExpenseCategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer une nouvelle catégorie de dépense"""
    category = ExpenseCategory(**category_data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


# ======================= STATUTS ==========================

@router.get("/statuts/fabrication", response_model=List[StatutFabricationResponse])
async def list_statuts_fabrication(
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des statuts de fabrication"""
    statuts = db.query(StatutFabrication).all()
    return statuts


@router.get("/statuts/livraison", response_model=List[StatutLivraisonResponse])
async def list_statuts_livraison(
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des statuts de livraison"""
    statuts = db.query(StatutLivraison).all()
    return statuts


@router.get("/statuts/appro", response_model=List[StatutApproResponse])
async def list_statuts_appro(
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des statuts d'approvisionnement"""
    statuts = db.query(StatutAppro).all()
    return statuts 