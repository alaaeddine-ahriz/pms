"""
Routes pour les ressources humaines
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_pagination_params, require_authenticated_user, get_current_user_id
from schemas.common import PaginationParams, PaginatedResponse, ResponseMessage
from schemas.hr import *
from models.hr import Employe, Task
from models.referentiels import FonctionEmploye
from models.documents import Document

router = APIRouter(prefix="/api/v1", tags=["Human Resources"])


# ======================= EMPLOYÉS ==========================

@router.get("/employees", response_model=List[EmployeResponse])
async def list_employees(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des employés avec pagination"""
    skip = (pagination.page - 1) * pagination.page_size
    employees = db.query(Employe).offset(skip).limit(pagination.page_size).all()
    return employees


@router.post("/employees", response_model=EmployeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee_data: EmployeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer un nouvel employé"""
    # Vérifier que le CIN n'existe pas déjà
    if employee_data.cin_numero:
        existing = db.query(Employe).filter(Employe.cin_numero == employee_data.cin_numero).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Employee with CIN {employee_data.cin_numero} already exists"
            )
    
    # Vérifier que la fonction existe
    if employee_data.id_fonction:
        fonction = db.query(FonctionEmploye).filter(FonctionEmploye.id_fonction == employee_data.id_fonction).first()
        if not fonction:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Function not found"
            )
    
    employee = Employe(**employee_data.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@router.get("/employees/{employee_id}", response_model=EmployeResponse)
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer un employé par ID"""
    employee = db.query(Employe).filter(Employe.id_employe == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return employee


@router.patch("/employees/{employee_id}", response_model=EmployeResponse)
async def update_employee(
    employee_id: int,
    employee_data: EmployeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Modifier un employé"""
    employee = db.query(Employe).filter(Employe.id_employe == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Mettre à jour uniquement les champs fournis
    update_data = employee_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)
    
    db.commit()
    db.refresh(employee)
    return employee


@router.post("/employees/{employee_id}/documents", response_model=ResponseMessage)
async def attach_employee_documents(
    employee_id: int,
    attach_request: AttachDocumentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Attacher des documents à un employé (CIN, permis, etc.)"""
    employee = db.query(Employe).filter(Employe.id_employe == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Pour l'instant, on ne fait que valider que les documents existent
    documents = db.query(Document).filter(Document.id_document.in_(attach_request.document_ids)).all()
    if len(documents) != len(attach_request.document_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more documents not found"
        )
    
    return ResponseMessage(
        message=f"Documents attached to employee {employee_id}",
        success=True
    )


# ======================= TÂCHES ==========================

@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des tâches avec pagination"""
    skip = (pagination.page - 1) * pagination.page_size
    tasks = db.query(Task).offset(skip).limit(pagination.page_size).all()
    return tasks


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer une nouvelle tâche"""
    # Séparer les assignés des autres données
    assignee_ids = task_data.assignee_ids
    task_dict = task_data.model_dump()
    task_dict.pop('assignee_ids', None)
    
    task = Task(**task_dict)
    db.add(task)
    db.flush()  # Pour obtenir l'ID sans commit
    
    # Assigner les employés si spécifiés
    if assignee_ids:
        assignees = db.query(Employe).filter(Employe.id_employe.in_(assignee_ids)).all()
        if len(assignees) != len(assignee_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more employees not found"
            )
        task.assignees.extend(assignees)
    
    db.commit()
    db.refresh(task)
    return task


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer une tâche par ID"""
    task = db.query(Task).filter(Task.id_task == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Modifier une tâche"""
    task = db.query(Task).filter(Task.id_task == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Mettre à jour uniquement les champs fournis
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    return task


@router.post("/tasks/{task_id}/assignees", response_model=ResponseMessage)
async def assign_task(
    task_id: int,
    assign_request: AssignTaskRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Assigner un employé à une tâche"""
    task = db.query(Task).filter(Task.id_task == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    employee = db.query(Employe).filter(Employe.id_employe == assign_request.employe_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Vérifier si déjà assigné
    if employee not in task.assignees:
        task.assignees.append(employee)
        db.commit()
    
    return ResponseMessage(
        message=f"Employee {assign_request.employe_id} assigned to task {task_id}",
        success=True
    )


@router.delete("/tasks/{task_id}/assignees/{employee_id}", response_model=ResponseMessage)
async def unassign_task(
    task_id: int,
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Désassigner un employé d'une tâche"""
    task = db.query(Task).filter(Task.id_task == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    employee = db.query(Employe).filter(Employe.id_employe == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    if employee in task.assignees:
        task.assignees.remove(employee)
        db.commit()
    
    return ResponseMessage(
        message=f"Employee {employee_id} unassigned from task {task_id}",
        success=True
    )


@router.post("/tasks/{task_id}/subtasks", response_model=ResponseMessage)
async def link_subtask(
    task_id: int,
    subtask_request: LinkSubtaskRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Lier une tâche enfant (sous-tâche)"""
    parent_task = db.query(Task).filter(Task.id_task == task_id).first()
    if not parent_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent task not found"
        )
    
    child_task = db.query(Task).filter(Task.id_task == subtask_request.child_task_id).first()
    if not child_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child task not found"
        )
    
    # Éviter les références circulaires
    if child_task == parent_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task cannot be its own subtask"
        )
    
    # Ajouter la relation parent-enfant
    if child_task not in parent_task.child_tasks:
        parent_task.child_tasks.append(child_task)
        db.commit()
    
    return ResponseMessage(
        message=f"Task {subtask_request.child_task_id} linked as subtask of {task_id}",
        success=True
    )


@router.post("/tasks/{task_id}/documents", response_model=ResponseMessage)
async def attach_task_documents(
    task_id: int,
    attach_request: AttachDocumentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Attacher des documents à une tâche"""
    task = db.query(Task).filter(Task.id_task == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
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
        if document not in task.documents:
            task.documents.append(document)
    
    db.commit()
    
    return ResponseMessage(
        message=f"Documents attached to task {task_id}",
        success=True
    ) 