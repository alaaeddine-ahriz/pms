"""
Routes pour la gestion des projets
"""
from typing import List
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from dependencies import get_pagination_params, require_authenticated_user
from schemas.common import PaginationParams, ResponseMessage
from schemas.projects import *
from models.projects import Projet, SiteClient
from models.finance import CaisseProjet, LedgerLine, Account
from models.hr import Employe
from models.vehicles import Voiture
from models.materials import Materiel

router = APIRouter(prefix="/api/v1", tags=["Projects"])


# ======================= SITES CLIENTS ==========================

@router.get("/sites", response_model=List[SiteClientResponse])
async def list_client_sites(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des sites clients avec pagination"""
    skip = (pagination.page - 1) * pagination.page_size
    sites = db.query(SiteClient).offset(skip).limit(pagination.page_size).all()
    return sites


@router.post("/sites", response_model=SiteClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client_site(
    site_data: SiteClientCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer un nouveau site client"""
    site = SiteClient(**site_data.model_dump())
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


# ======================= PROJETS ==========================

@router.get("/projects", response_model=List[ProjetResponse])
async def list_projects(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des projets avec pagination"""
    skip = (pagination.page - 1) * pagination.page_size
    projects = db.query(Projet).offset(skip).limit(pagination.page_size).all()
    return projects


@router.post("/projects", response_model=ProjetResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjetCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer un nouveau projet"""
    # Vérifier que le chef de chantier existe
    if project_data.id_chef_chantier:
        chef = db.query(Employe).filter(Employe.id_employe == project_data.id_chef_chantier).first()
        if not chef:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project manager not found"
            )
    
    project = Projet(**project_data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/projects/{project_id}", response_model=ProjetResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer un projet par ID"""
    project = db.query(Projet).filter(Projet.id_projet == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project


@router.patch("/projects/{project_id}", response_model=ProjetResponse)
async def update_project(
    project_id: int,
    project_data: ProjetUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Modifier un projet"""
    project = db.query(Projet).filter(Projet.id_projet == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Mettre à jour uniquement les champs fournis
    update_data = project_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    return project


@router.post("/projects/{project_id}/vehicles", response_model=ResponseMessage)
async def link_project_vehicle(
    project_id: int,
    vehicle_request: LinkVehicleRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Lier un véhicule à un projet"""
    project = db.query(Projet).filter(Projet.id_projet == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    vehicle = db.query(Voiture).filter(Voiture.id_voiture == vehicle_request.vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    # Ajouter le véhicule s'il n'est pas déjà lié
    if vehicle not in project.voitures:
        project.voitures.append(vehicle)
        db.commit()
    
    return ResponseMessage(
        message=f"Vehicle {vehicle_request.vehicle_id} linked to project {project_id}",
        success=True
    )


@router.post("/projects/{project_id}/materials", response_model=ResponseMessage)
async def link_project_material(
    project_id: int,
    material_request: LinkMaterialRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Lier du matériel à un projet"""
    project = db.query(Projet).filter(Projet.id_projet == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    material = db.query(Materiel).filter(Materiel.id_materiel == material_request.material_id).first()
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    
    # Ajouter le matériel s'il n'est pas déjà lié
    if material not in project.materiel:
        project.materiel.append(material)
        db.commit()
    
    return ResponseMessage(
        message=f"Material {material_request.material_id} linked to project {project_id}",
        success=True
    )


@router.post("/projects/{project_id}/documents", response_model=ResponseMessage)
async def attach_project_documents(
    project_id: int,
    attach_request: AttachDocumentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Attacher des documents à un projet"""
    project = db.query(Projet).filter(Projet.id_projet == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Vérifier que tous les documents existent
    from models.documents import Document
    documents = db.query(Document).filter(Document.id_document.in_(attach_request.document_ids)).all()
    if len(documents) != len(attach_request.document_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more documents not found"
        )
    
    # Attacher les documents
    for document in documents:
        if document not in project.documents:
            project.documents.append(document)
    
    db.commit()
    
    return ResponseMessage(
        message=f"Documents attached to project {project_id}",
        success=True
    )


# ======================= CAISSE PROJET ==========================

@router.get("/projects/{project_id}/cash/balance", response_model=CaisseBalanceResponse)
async def get_project_cash_balance(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer le solde actuel de la caisse d'un projet"""
    project = db.query(Projet).filter(Projet.id_projet == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    caisse = db.query(CaisseProjet).filter(CaisseProjet.id_projet == project_id).first()
    if not caisse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project cash not found"
        )
    
    # Calculer le solde en sommant toutes les lignes du grand livre pour ce compte
    query = text("""
        SELECT 
            SUM(
                CASE 
                    WHEN debit_account = :account_id THEN amount_minor
                    WHEN credit_account = :account_id THEN -amount_minor
                    ELSE 0
                END
            ) as balance_minor,
            MAX(date_op) as last_transaction
        FROM ledger_line
        WHERE debit_account = :account_id OR credit_account = :account_id
    """)
    
    result = db.execute(query, {"account_id": caisse.id_account}).first()
    balance_minor = result.balance_minor or 0
    
    # Convertir en unités principales (diviser par 100 pour les centimes)
    balance = Decimal(balance_minor) / 100
    
    return CaisseBalanceResponse(
        balance=balance,
        currency="MAD",  # TODO: Récupérer la devise du projet
        last_updated=result.last_transaction.isoformat() if result.last_transaction else None
    )


@router.post("/projects/{project_id}/cash/top-up", response_model=ResponseMessage)
async def top_up_project_cash(
    project_id: int,
    top_up_data: CaisseTopUpRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Alimentation de la caisse d'un projet"""
    project = db.query(Projet).filter(Projet.id_projet == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    caisse = db.query(CaisseProjet).filter(CaisseProjet.id_projet == project_id).first()
    if not caisse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project cash not found"
        )
    
    # TODO: Implémenter la logique d'alimentation de caisse
    # Créer une ligne de grand livre pour l'alimentation
    amount_minor = int(top_up_data.amount * 100)  # Convertir en centimes
    
    # Pour l'instant, on simule juste la réponse
    return ResponseMessage(
        message=f"Cash top-up of {top_up_data.amount} {top_up_data.currency} added to project {project_id}",
        success=True
    )


@router.post("/projects/{project_id}/cash/expense", response_model=ResponseMessage)
async def create_project_cash_expense(
    project_id: int,
    expense_data: CaisseExpenseRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer une dépense sur la caisse d'un projet"""
    project = db.query(Projet).filter(Projet.id_projet == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    caisse = db.query(CaisseProjet).filter(CaisseProjet.id_projet == project_id).first()
    if not caisse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project cash not found"
        )
    
    # Vérifier que la catégorie existe
    from models.referentiels import ExpenseCategory
    category = db.query(ExpenseCategory).filter(ExpenseCategory.id_cat == expense_data.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expense category not found"
        )
    
    # TODO: Implémenter la logique de dépense de caisse
    # Créer une ligne de grand livre pour la dépense
    amount_minor = int(expense_data.amount * 100)  # Convertir en centimes
    
    # Pour l'instant, on simule juste la réponse
    return ResponseMessage(
        message=f"Cash expense of {expense_data.amount} {expense_data.currency} recorded for project {project_id}",
        success=True
    )


@router.get("/projects/{project_id}/cash/ledger", response_model=List[dict])
async def get_project_cash_ledger(
    project_id: int,
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer le grand livre de la caisse d'un projet (paginé)"""
    project = db.query(Projet).filter(Projet.id_projet == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    caisse = db.query(CaisseProjet).filter(CaisseProjet.id_projet == project_id).first()
    if not caisse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project cash not found"
        )
    
    # Récupérer les lignes du grand livre pour ce compte
    skip = (pagination.page - 1) * pagination.page_size
    
    ledger_lines = db.query(LedgerLine).filter(
        (LedgerLine.debit_account == caisse.id_account) |
        (LedgerLine.credit_account == caisse.id_account)
    ).order_by(LedgerLine.date_op.desc()).offset(skip).limit(pagination.page_size).all()
    
    # Formatter la réponse
    ledger_data = []
    for line in ledger_lines:
        entry_type = "CREDIT" if line.debit_account == caisse.id_account else "DEBIT"
        amount = Decimal(line.amount_minor) / 100
        
        ledger_data.append({
            "id_line": line.id_line,
            "date_op": line.date_op.isoformat(),
            "type": entry_type,
            "amount": float(amount),
            "currency": line.currency,
            "memo": line.memo,
            "category": line.category.libelle if line.category else None
        })
    
    return ledger_data 