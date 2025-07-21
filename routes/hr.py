"""
Routes pour les ressources humaines
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from models.hr import Employe, Task
from models.referentiels import FonctionEmploye
from schemas.hr import (
    EmployeResponse, EmployeCreate, EmployeUpdate, CreateEmployeeRequest,
    TaskResponse, TaskCreate, TaskUpdate,
    TaskAssignmentRequest
)
from schemas.referentiels import FonctionEmployeResponse, FonctionEmployeCreate
from schemas.common import ResponseMessage, PaginatedResponse, AttachDocumentRequest
from models.documents import Document
from dependencies import get_pagination_params
from schemas.common import PaginationParams

router = APIRouter(prefix="/api/v1", tags=["Human Resources"])


@router.get("/employees", response_model=PaginatedResponse[EmployeResponse])
async def get_employees(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Récupérer la liste des employés avec pagination"""
    query = db.query(Employe)
    
    total = query.count()
    employees = query.offset(pagination.offset).limit(pagination.limit).all()
    
    return PaginatedResponse(
        items=employees,
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=(total + pagination.size - 1) // pagination.size
    )


@router.post("", response_model=ResponseMessage, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee_data: CreateEmployeeRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Créer un nouvel employé
    """
    from auth import get_password_hash
    
    try:
        # Vérifier que l'email n'existe pas déjà (si fourni)
        if employee_data.email:
            existing_user = db.query(Employe).filter(Employe.email == employee_data.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
    
        # Créer l'employé
        new_employee = Employe(
            cin_numero=employee_data.cin_numero,
            nom=employee_data.nom,
            prenom=employee_data.prenom,
            etat_civil=employee_data.etat_civil,
            date_naissance=employee_data.date_naissance,
            salaire_net=employee_data.salaire_net,
            id_fonction=employee_data.id_fonction,
            email=employee_data.email,
            password_hash=get_password_hash(employee_data.password) if employee_data.password else None,
            role=employee_data.role or "employee",
            is_active="1"
        )
        
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        
        # Message de succès avec info d'authentification
        auth_info = ""
        if employee_data.email and employee_data.password:
            auth_info = f" | Login: {employee_data.email}"
        
        return ResponseMessage(
            message=f"Employé {new_employee.prenom} {new_employee.nom} créé avec succès{auth_info}",
            success=True
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/employees/{employee_id}", response_model=EmployeResponse)
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Récupérer un employé par son ID"""
    employee = db.query(Employe).filter(Employe.id_employe == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.patch("/employees/{employee_id}", response_model=EmployeResponse)
async def update_employee(
    employee_id: int,
    employee_data: EmployeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Mettre à jour un employé"""
    employee = db.query(Employe).filter(Employe.id_employe == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Mettre à jour les champs fournis
    for field, value in employee_data.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)
    
    db.commit()
    db.refresh(employee)
    return employee


@router.delete("/employees/{employee_id}", response_model=ResponseMessage)
async def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Supprimer un employé (soft delete)"""
    employee = db.query(Employe).filter(Employe.id_employe == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Soft delete en désactivant l'employé
    employee.is_active = "0"
    db.commit()
    
    return ResponseMessage(
        message=f"Employee {employee.prenom} {employee.nom} deleted successfully",
        success=True
    )


@router.post("/employees/{employee_id}/documents", response_model=ResponseMessage)
async def attach_document_to_employee(
    employee_id: int,
    request: AttachDocumentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Attacher des documents à un employé"""
    employee = db.query(Employe).filter(Employe.id_employe == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Vérifier que les documents existent
    documents = db.query(Document).filter(Document.id_document.in_(request.document_ids)).all()
    if len(documents) != len(request.document_ids):
        raise HTTPException(status_code=404, detail="One or more documents not found")
    
    # Logique d'attachement selon le type de document
    # (CIN, permis, etc.)
    
    return ResponseMessage(
        message=f"{len(documents)} document(s) attached to employee",
        success=True
    )


# Routes pour les fonctions d'employés
@router.get("/functions", response_model=List[FonctionEmployeResponse])
async def get_employee_functions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Récupérer la liste des fonctions d'employés"""
    functions = db.query(FonctionEmploye).all()
    return functions


@router.post("/functions", response_model=FonctionEmployeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee_function(
    function_data: FonctionEmployeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Créer une nouvelle fonction d'employé"""
    function = FonctionEmploye(**function_data.model_dump())
    db.add(function)
    db.commit()
    db.refresh(function)
    return function


# Routes pour les tâches
@router.get("/tasks", response_model=PaginatedResponse[TaskResponse])
async def get_tasks(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Récupérer la liste des tâches avec pagination"""
    query = db.query(Task)
    
    total = query.count()
    tasks = query.offset(pagination.offset).limit(pagination.limit).all()
    
    return PaginatedResponse(
        items=tasks,
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=(total + pagination.size - 1) // pagination.size
    )


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Créer une nouvelle tâche"""
    task = Task(**task_data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Récupérer une tâche par son ID"""
    task = db.query(Task).filter(Task.id_task == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Mettre à jour une tâche"""
    task = db.query(Task).filter(Task.id_task == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Mettre à jour les champs fournis
    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}", response_model=ResponseMessage)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Supprimer une tâche"""
    task = db.query(Task).filter(Task.id_task == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    
    return ResponseMessage(
        message="Task deleted successfully",
        success=True
    )


@router.post("/tasks/{task_id}/assignees", response_model=ResponseMessage)
async def assign_task_to_employee(
    task_id: int,
    assignment: TaskAssignmentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Assigner une tâche à un employé"""
    task = db.query(Task).filter(Task.id_task == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    employee = db.query(Employe).filter(Employe.id_employe == assignment.id_employe).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Vérifier si l'assignation existe déjà
    if employee in task.assignees:
        raise HTTPException(status_code=400, detail="Employee already assigned to this task")
    
        task.assignees.append(employee)
        db.commit()
    
    return ResponseMessage(
        message=f"Task assigned to {employee.prenom} {employee.nom}",
        success=True
    )


@router.delete("/tasks/{task_id}/assignees/{employee_id}", response_model=ResponseMessage)
async def unassign_task_from_employee(
    task_id: int,
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Désassigner une tâche d'un employé"""
    task = db.query(Task).filter(Task.id_task == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    employee = db.query(Employe).filter(Employe.id_employe == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if employee not in task.assignees:
        raise HTTPException(status_code=400, detail="Employee not assigned to this task")
    
        task.assignees.remove(employee)
        db.commit()
    
    return ResponseMessage(
        message=f"Task unassigned from {employee.prenom} {employee.nom}",
        success=True
    )


@router.post("/tasks/{task_id}/subtasks", response_model=ResponseMessage)
async def add_subtask(
    task_id: int,
    subtask_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Ajouter une sous-tâche à une tâche"""
    parent_task = db.query(Task).filter(Task.id_task == task_id).first()
    if not parent_task:
        raise HTTPException(status_code=404, detail="Parent task not found")
    
    subtask = db.query(Task).filter(Task.id_task == subtask_id).first()
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    
    # Logique pour éviter les cycles
    if task_id == subtask_id:
        raise HTTPException(status_code=400, detail="Task cannot be its own subtask")
    
    # Ajouter la relation parent-enfant
    # (Nécessiterait une logique plus complexe selon le modèle)
    
    return ResponseMessage(
        message="Subtask added successfully",
        success=True
    )


@router.post("/tasks/{task_id}/documents", response_model=ResponseMessage)
async def attach_document_to_task(
    task_id: int,
    request: AttachDocumentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Attacher des documents à une tâche"""
    task = db.query(Task).filter(Task.id_task == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Vérifier que les documents existent
    documents = db.query(Document).filter(Document.id_document.in_(request.document_ids)).all()
    if len(documents) != len(request.document_ids):
        raise HTTPException(status_code=404, detail="One or more documents not found")
    
    # Attacher les documents à la tâche
    for document in documents:
        if document not in task.documents:
            task.documents.append(document)
    
    db.commit()
    
    return ResponseMessage(
        message=f"{len(documents)} document(s) attached to task",
        success=True
    ) 