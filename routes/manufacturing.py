"""
Routes pour la gestion de la fabrication
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_pagination_params, require_authenticated_user
from schemas.common import PaginationParams, ResponseMessage, AttachDocumentRequest
from schemas.manufacturing import *
from models.manufacturing import NomenclatureFabrication, OrdreFabrication, OFDocument
from models.products import Produit
from models.projects import Projet
from models.referentiels import StatutFabrication
from models.documents import Document

router = APIRouter(prefix="/api/v1", tags=["Manufacturing"])


# ======================= NOMENCLATURES (BOM) ==========================

@router.get("/bom", response_model=List[NomenclatureFabricationResponse])
async def list_bom(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des nomenclatures de fabrication avec pagination"""
    skip = (pagination.page - 1) * pagination.page_size
    boms = db.query(NomenclatureFabrication).offset(skip).limit(pagination.page_size).all()
    return boms


@router.post("/bom", response_model=NomenclatureFabricationResponse, status_code=status.HTTP_201_CREATED)
async def create_bom(
    bom_data: NomenclatureFabricationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer une nouvelle nomenclature de fabrication"""
    bom = NomenclatureFabrication(**bom_data.model_dump())
    db.add(bom)
    db.commit()
    db.refresh(bom)
    return bom


@router.get("/bom/{bom_id}", response_model=NomenclatureFabricationResponse)
async def get_bom(
    bom_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer une nomenclature par ID"""
    bom = db.query(NomenclatureFabrication).filter(NomenclatureFabrication.id_nomenclature == bom_id).first()
    if not bom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BOM not found"
        )
    return bom


@router.patch("/bom/{bom_id}", response_model=NomenclatureFabricationResponse)
async def update_bom(
    bom_id: int,
    bom_data: NomenclatureFabricationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Modifier une nomenclature"""
    bom = db.query(NomenclatureFabrication).filter(NomenclatureFabrication.id_nomenclature == bom_id).first()
    if not bom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BOM not found"
        )
    
    # Mettre à jour uniquement les champs fournis
    update_data = bom_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bom, field, value)
    
    db.commit()
    db.refresh(bom)
    return bom


@router.post("/bom/{bom_id}/products", response_model=ResponseMessage)
async def add_bom_product(
    bom_id: int,
    product_request: AddBOMProductRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Ajouter un produit/composant à une nomenclature"""
    bom = db.query(NomenclatureFabrication).filter(NomenclatureFabrication.id_nomenclature == bom_id).first()
    if not bom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BOM not found"
        )
    
    product = db.query(Produit).filter(Produit.id_produit == product_request.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Ajouter le produit s'il n'est pas déjà dans la nomenclature
    if product not in bom.produits:
        bom.produits.append(product)
        db.commit()
    
    return ResponseMessage(
        message=f"Product {product_request.product_id} added to BOM {bom_id} with quantity {product_request.qty}",
        success=True
    )


# ======================= ORDRES DE FABRICATION ==========================

@router.get("/orders/fabrication", response_model=List[OrdreFabricationResponse])
async def list_fabrication_orders(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des ordres de fabrication avec pagination"""
    skip = (pagination.page - 1) * pagination.page_size
    orders = db.query(OrdreFabrication).offset(skip).limit(pagination.page_size).all()
    return orders


@router.post("/orders/fabrication", response_model=OrdreFabricationResponse, status_code=status.HTTP_201_CREATED)
async def create_fabrication_order(
    order_data: OrdreFabricationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer un nouvel ordre de fabrication"""
    # Vérifier que le projet existe si spécifié
    if order_data.id_projet:
        project = db.query(Projet).filter(Projet.id_projet == order_data.id_projet).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project not found"
            )
    
    # Vérifier que le statut existe si spécifié
    if order_data.id_statut_fabrication:
        status_fab = db.query(StatutFabrication).filter(StatutFabrication.id_statut == order_data.id_statut_fabrication).first()
        if not status_fab:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Fabrication status not found"
            )
    
    order = OrdreFabrication(**order_data.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("/orders/fabrication/{order_id}", response_model=OrdreFabricationResponse)
async def get_fabrication_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer un ordre de fabrication par ID"""
    order = db.query(OrdreFabrication).filter(OrdreFabrication.id_of == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fabrication order not found"
        )
    return order


@router.patch("/orders/fabrication/{order_id}", response_model=OrdreFabricationResponse)
async def update_fabrication_order(
    order_id: int,
    order_data: OrdreFabricationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Modifier un ordre de fabrication"""
    order = db.query(OrdreFabrication).filter(OrdreFabrication.id_of == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fabrication order not found"
        )
    
    # Mettre à jour uniquement les champs fournis
    update_data = order_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    
    db.commit()
    db.refresh(order)
    return order


@router.post("/orders/fabrication/{order_id}/bom", response_model=ResponseMessage)
async def link_bom_to_order(
    order_id: int,
    bom_request: LinkBOMRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Lier une nomenclature (BOM) à un ordre de fabrication avec quantité"""
    order = db.query(OrdreFabrication).filter(OrdreFabrication.id_of == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fabrication order not found"
        )
    
    bom = db.query(NomenclatureFabrication).filter(NomenclatureFabrication.id_nomenclature == bom_request.nomenclature_id).first()
    if not bom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BOM not found"
        )
    
    # Ajouter la nomenclature s'elle n'est pas déjà liée
    if bom not in order.nomenclatures:
        order.nomenclatures.append(bom)
        db.commit()
    
    return ResponseMessage(
        message=f"BOM {bom_request.nomenclature_id} linked to fabrication order {order_id} with quantity {bom_request.qty}",
        success=True
    )


@router.post("/orders/fabrication/{order_id}/documents", response_model=ResponseMessage)
async def upload_fabrication_progress(
    order_id: int,
    attach_request: AttachDocumentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Upload photo avancement/réalisation pour un ordre de fabrication"""
    order = db.query(OrdreFabrication).filter(OrdreFabrication.id_of == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fabrication order not found"
        )
    
    # Vérifier que tous les documents existent
    documents = db.query(Document).filter(Document.id_document.in_(attach_request.document_ids)).all()
    if len(documents) != len(attach_request.document_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more documents not found"
        )
    
    # Créer les liens OF-Document avec type de photo
    for document in documents:
        of_doc = OFDocument(
            id_of=order_id,
            id_document=document.id_document,
            type_photo="AVANCEMENT"  # Par défaut, peut être paramétré
        )
        db.add(of_doc)
    
    db.commit()
    
    return ResponseMessage(
        message=f"Progress photos uploaded for fabrication order {order_id}",
        success=True
    )


@router.patch("/orders/fabrication/{order_id}/status", response_model=ResponseMessage)
async def update_fabrication_status(
    order_id: int,
    status_request: UpdateStatusRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Mettre à jour le statut de production d'un ordre de fabrication"""
    order = db.query(OrdreFabrication).filter(OrdreFabrication.id_of == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fabrication order not found"
        )
    
    # Vérifier que le statut existe
    status_fab = db.query(StatutFabrication).filter(StatutFabrication.id_statut == status_request.status_id).first()
    if not status_fab:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fabrication status not found"
        )
    
    order.id_statut_fabrication = status_request.status_id
    db.commit()
    
    return ResponseMessage(
        message=f"Fabrication order {order_id} status updated to {status_fab.libelle}",
        success=True
    ) 