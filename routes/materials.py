"""
Routes pour la gestion du matériel
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_pagination_params, require_authenticated_user
from schemas.common import PaginationParams, ResponseMessage
from schemas.materials import *
from models.materials import Materiel
from models.documents import Document

router = APIRouter(prefix="/api/v1", tags=["Materials"])


@router.get("/materials", response_model=List[MaterielResponse])
async def list_materials(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste du matériel avec pagination"""
    skip = (pagination.page - 1) * pagination.page_size
    materials = db.query(Materiel).offset(skip).limit(pagination.page_size).all()
    return materials


@router.post("/materials", response_model=MaterielResponse, status_code=status.HTTP_201_CREATED)
async def create_material(
    material_data: MaterielCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer un nouveau matériel"""
    # Vérifier que le document de facture existe si spécifié
    if material_data.id_facture:
        invoice_doc = db.query(Document).filter(Document.id_document == material_data.id_facture).first()
        if not invoice_doc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invoice document not found"
            )
    
    material = Materiel(**material_data.model_dump())
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


@router.get("/materials/{material_id}", response_model=MaterielResponse)
async def get_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer un matériel par ID"""
    material = db.query(Materiel).filter(Materiel.id_materiel == material_id).first()
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    return material


@router.patch("/materials/{material_id}", response_model=MaterielResponse)
async def update_material(
    material_id: int,
    material_data: MaterielUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Modifier un matériel"""
    material = db.query(Materiel).filter(Materiel.id_materiel == material_id).first()
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    
    # Mettre à jour uniquement les champs fournis
    update_data = material_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(material, field, value)
    
    db.commit()
    db.refresh(material)
    return material


@router.post("/materials/{material_id}/documents", response_model=ResponseMessage)
async def attach_material_documents(
    material_id: int,
    attach_request: AttachDocumentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Attacher des documents à un matériel"""
    material = db.query(Materiel).filter(Materiel.id_materiel == material_id).first()
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    
    # Vérifier que tous les documents existent
    documents = db.query(Document).filter(Document.id_document.in_(attach_request.document_ids)).all()
    if len(documents) != len(attach_request.document_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more documents not found"
        )
    
    # Attacher les documents
    for document in documents:
        if document not in material.documents:
            material.documents.append(document)
    
    db.commit()
    
    return ResponseMessage(
        message=f"Documents attached to material {material_id}",
        success=True
    ) 