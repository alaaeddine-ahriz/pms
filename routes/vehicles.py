"""
Routes pour la gestion des véhicules
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_pagination_params, require_authenticated_user
from schemas.common import PaginationParams, ResponseMessage
from schemas.vehicles import *
from models.vehicles import Voiture, VoitureKmLog, VoitureConducteur
from models.hr import Employe

router = APIRouter(prefix="/api/v1", tags=["Vehicles"])


# ======================= VÉHICULES ==========================

@router.get("/vehicles", response_model=List[VoitureResponse])
async def list_vehicles(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des véhicules avec pagination"""
    skip = (pagination.page - 1) * pagination.page_size
    vehicles = db.query(Voiture).offset(skip).limit(pagination.page_size).all()
    return vehicles


@router.post("/vehicles", response_model=VoitureResponse, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_data: VoitureCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer un nouveau véhicule"""
    # Vérifier que l'immatriculation n'existe pas déjà
    if vehicle_data.immatriculation:
        existing = db.query(Voiture).filter(Voiture.immatriculation == vehicle_data.immatriculation).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Vehicle with registration {vehicle_data.immatriculation} already exists"
            )
    
    vehicle = Voiture(**vehicle_data.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


@router.get("/vehicles/{vehicle_id}", response_model=VoitureResponse)
async def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer un véhicule par ID"""
    vehicle = db.query(Voiture).filter(Voiture.id_voiture == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    return vehicle


@router.patch("/vehicles/{vehicle_id}", response_model=VoitureResponse)
async def update_vehicle(
    vehicle_id: int,
    vehicle_data: VoitureUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Modifier un véhicule"""
    vehicle = db.query(Voiture).filter(Voiture.id_voiture == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    # Mettre à jour uniquement les champs fournis
    update_data = vehicle_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(vehicle, field, value)
    
    db.commit()
    db.refresh(vehicle)
    return vehicle


# ======================= RELEVÉS KILOMÉTRIQUES ==========================

@router.post("/vehicles/{vehicle_id}/km-log", response_model=VoitureKmLogResponse, status_code=status.HTTP_201_CREATED)
async def add_km_log(
    vehicle_id: int,
    km_log_data: VoitureKmLogCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Ajouter un relevé kilométrique"""
    vehicle = db.query(Voiture).filter(Voiture.id_voiture == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    # Vérifier qu'il n'y a pas déjà un relevé pour cette date
    existing = db.query(VoitureKmLog).filter(
        VoitureKmLog.id_voiture == vehicle_id,
        VoitureKmLog.date_releve == km_log_data.date_releve
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Km log already exists for {km_log_data.date_releve}"
        )
    
    km_log = VoitureKmLog(
        id_voiture=vehicle_id,
        **km_log_data.model_dump()
    )
    db.add(km_log)
    db.commit()
    db.refresh(km_log)
    return km_log


# ======================= CONDUCTEURS ==========================

@router.post("/vehicles/{vehicle_id}/drivers", response_model=VoitureConducteurResponse, status_code=status.HTTP_201_CREATED)
async def assign_driver(
    vehicle_id: int,
    driver_data: VoitureConducteurCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Assigner un conducteur à un véhicule"""
    vehicle = db.query(Voiture).filter(Voiture.id_voiture == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    employee = db.query(Employe).filter(Employe.id_employe == driver_data.employe_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Vérifier qu'il n'y a pas déjà une assignation active pour ce véhicule
    active_assignment = db.query(VoitureConducteur).filter(
        VoitureConducteur.id_voiture == vehicle_id,
        VoitureConducteur.date_fin.is_(None)
    ).first()
    
    if active_assignment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle already has an active driver assignment"
        )
    
    assignment = VoitureConducteur(
        id_voiture=vehicle_id,
        id_employe=driver_data.employe_id,
        date_debut=driver_data.date_start
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


@router.patch("/vehicles/{vehicle_id}/drivers/{employee_id}", response_model=VoitureConducteurResponse)
async def close_driver_assignment(
    vehicle_id: int,
    employee_id: int,
    update_data: VoitureConducteurUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Clôturer une assignation de conducteur (date_fin)"""
    assignment = db.query(VoitureConducteur).filter(
        VoitureConducteur.id_voiture == vehicle_id,
        VoitureConducteur.id_employe == employee_id,
        VoitureConducteur.date_fin.is_(None)
    ).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active driver assignment not found"
        )
    
    if update_data.date_end:
        assignment.date_fin = update_data.date_end
        db.commit()
        db.refresh(assignment)
    
    return assignment 