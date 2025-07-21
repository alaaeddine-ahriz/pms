"""
Routes pour la logistique et les approvisionnements
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_pagination_params, require_authenticated_user
from schemas.common import PaginationParams, ResponseMessage
from schemas.logistics import *
from models.logistics import Livraison, SupplyRequest, SupplyRequestTracking
from models.products import StockMove, Produit
from models.hr import Employe
from models.referentiels import StatutLivraison, StatutAppro

router = APIRouter(prefix="/api/v1", tags=["Logistics"])


# ======================= LIVRAISONS ==========================

@router.get("/deliveries", response_model=List[LivraisonResponse])
async def list_deliveries(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des livraisons avec pagination"""
    skip = (pagination.page - 1) * pagination.page_size
    deliveries = db.query(Livraison).offset(skip).limit(pagination.page_size).all()
    return deliveries


@router.post("/deliveries", response_model=LivraisonResponse, status_code=status.HTTP_201_CREATED)
async def create_delivery(
    delivery_data: LivraisonCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer une nouvelle livraison (wraps deux mouvements de stock)"""
    # Vérifier que les mouvements de stock existent
    if delivery_data.id_move_out:
        move_out = db.query(StockMove).filter(StockMove.id_move == delivery_data.id_move_out).first()
        if not move_out:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Outbound stock move not found"
            )
    
    if delivery_data.id_move_in:
        move_in = db.query(StockMove).filter(StockMove.id_move == delivery_data.id_move_in).first()
        if not move_in:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inbound stock move not found"
            )
    
    # Vérifier le statut si spécifié
    if delivery_data.id_statut_livraison:
        status_delivery = db.query(StatutLivraison).filter(StatutLivraison.id_statut == delivery_data.id_statut_livraison).first()
        if not status_delivery:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delivery status not found"
            )
    
    # Vérifier le livreur si spécifié
    if delivery_data.id_livreur:
        driver = db.query(Employe).filter(Employe.id_employe == delivery_data.id_livreur).first()
        if not driver:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Driver not found"
            )
    
    delivery = Livraison(**delivery_data.model_dump())
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    return delivery


@router.get("/deliveries/{delivery_id}", response_model=LivraisonResponse)
async def get_delivery(
    delivery_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer une livraison par ID"""
    delivery = db.query(Livraison).filter(Livraison.id_livraison == delivery_id).first()
    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery not found"
        )
    return delivery


@router.patch("/deliveries/{delivery_id}", response_model=LivraisonResponse)
async def update_delivery(
    delivery_id: int,
    delivery_data: LivraisonUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Modifier une livraison"""
    delivery = db.query(Livraison).filter(Livraison.id_livraison == delivery_id).first()
    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery not found"
        )
    
    # Mettre à jour uniquement les champs fournis
    update_data = delivery_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(delivery, field, value)
    
    db.commit()
    db.refresh(delivery)
    return delivery


@router.patch("/deliveries/{delivery_id}/status", response_model=ResponseMessage)
async def update_delivery_status(
    delivery_id: int,
    status_request: UpdateDeliveryStatusRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Mettre à jour le statut d'une livraison"""
    delivery = db.query(Livraison).filter(Livraison.id_livraison == delivery_id).first()
    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery not found"
        )
    
    # Vérifier que le statut existe
    status_delivery = db.query(StatutLivraison).filter(StatutLivraison.id_statut == status_request.status_id).first()
    if not status_delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery status not found"
        )
    
    delivery.id_statut_livraison = status_request.status_id
    db.commit()
    
    return ResponseMessage(
        message=f"Delivery {delivery_id} status updated to {status_delivery.libelle}",
        success=True
    )


# ======================= DEMANDES D'APPROVISIONNEMENT ==========================

@router.get("/supply-requests", response_model=List[SupplyRequestResponse])
async def list_supply_requests(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des demandes d'approvisionnement avec pagination"""
    skip = (pagination.page - 1) * pagination.page_size
    requests = db.query(SupplyRequest).offset(skip).limit(pagination.page_size).all()
    return requests


@router.post("/supply-requests", response_model=SupplyRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_supply_request(
    request_data: SupplyRequestCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer une nouvelle demande d'approvisionnement"""
    # Vérifier le demandeur si spécifié
    if request_data.id_demandeur:
        requester = db.query(Employe).filter(Employe.id_employe == request_data.id_demandeur).first()
        if not requester:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Requester not found"
            )
    
    # Vérifier le statut si spécifié
    if request_data.id_statut_appro:
        status_appro = db.query(StatutAppro).filter(StatutAppro.id_statut == request_data.id_statut_appro).first()
        if not status_appro:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Supply status not found"
            )
    
    supply_request = SupplyRequest(**request_data.model_dump())
    db.add(supply_request)
    db.commit()
    db.refresh(supply_request)
    return supply_request


@router.get("/supply-requests/{request_id}", response_model=SupplyRequestResponse)
async def get_supply_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer une demande d'approvisionnement par ID"""
    supply_request = db.query(SupplyRequest).filter(SupplyRequest.id_supply_request == request_id).first()
    if not supply_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supply request not found"
        )
    return supply_request


@router.patch("/supply-requests/{request_id}", response_model=SupplyRequestResponse)
async def update_supply_request(
    request_id: int,
    request_data: SupplyRequestUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Modifier une demande d'approvisionnement"""
    supply_request = db.query(SupplyRequest).filter(SupplyRequest.id_supply_request == request_id).first()
    if not supply_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supply request not found"
        )
    
    # Mettre à jour uniquement les champs fournis
    update_data = request_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(supply_request, field, value)
    
    db.commit()
    db.refresh(supply_request)
    return supply_request


@router.post("/supply-requests/{request_id}/products", response_model=ResponseMessage)
async def add_supply_request_product(
    request_id: int,
    product_request: AddSupplyProductRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Ajouter un produit à une demande d'approvisionnement"""
    supply_request = db.query(SupplyRequest).filter(SupplyRequest.id_supply_request == request_id).first()
    if not supply_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supply request not found"
        )
    
    product = db.query(Produit).filter(Produit.id_produit == product_request.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Ajouter le produit s'il n'est pas déjà dans la demande
    if product not in supply_request.produits:
        supply_request.produits.append(product)
        db.commit()
    
    return ResponseMessage(
        message=f"Product {product_request.product_id} added to supply request {request_id} with quantity {product_request.qty}",
        success=True
    )


@router.post("/supply-requests/{request_id}/tracking", response_model=SupplyRequestTrackingResponse, status_code=status.HTTP_201_CREATED)
async def add_supply_request_tracking(
    request_id: int,
    tracking_data: SupplyRequestTrackingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Ajouter un événement de suivi à une demande d'approvisionnement"""
    supply_request = db.query(SupplyRequest).filter(SupplyRequest.id_supply_request == request_id).first()
    if not supply_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supply request not found"
        )
    
    # Vérifier que le statut existe
    status_appro = db.query(StatutAppro).filter(StatutAppro.id_statut == tracking_data.id_statut).first()
    if not status_appro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supply status not found"
        )
    
    tracking = SupplyRequestTracking(
        id_supply_request=request_id,
        **tracking_data.model_dump()
    )
    db.add(tracking)
    db.commit()
    db.refresh(tracking)
    return tracking 