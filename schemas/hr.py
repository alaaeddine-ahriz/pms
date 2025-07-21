"""
Schémas pour les ressources humaines
"""
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, Field
from .common import BaseSchema, TimestampMixin


class EmployeBase(BaseSchema):
    """Schéma de base pour les employés"""
    cin_numero: Optional[str] = Field(None, max_length=20, description="Numéro CIN")
    nom: str = Field(..., description="Nom")
    prenom: str = Field(..., description="Prénom")
    etat_civil: Optional[str] = Field(None, description="État civil")
    date_naissance: Optional[date] = Field(None, description="Date de naissance")
    salaire_net: Optional[Decimal] = Field(None, description="Salaire net")
    id_fonction: Optional[int] = Field(None, description="ID fonction")


class EmployeCreate(EmployeBase):
    """Schéma pour créer un employé"""
    id_doc_cin: Optional[int] = Field(None, description="ID document CIN")
    id_doc_permis: Optional[int] = Field(None, description="ID document permis")


class EmployeUpdate(BaseSchema):
    """Schéma pour modifier un employé"""
    cin_numero: Optional[str] = None
    nom: Optional[str] = None
    prenom: Optional[str] = None
    etat_civil: Optional[str] = None
    date_naissance: Optional[date] = None
    salaire_net: Optional[Decimal] = None
    id_fonction: Optional[int] = None
    id_doc_cin: Optional[int] = None
    id_doc_permis: Optional[int] = None


class EmployeResponse(EmployeBase, TimestampMixin):
    """Schéma de réponse pour un employé"""
    id_employe: int
    id_doc_cin: Optional[int] = None
    id_doc_permis: Optional[int] = None
    fonction: Optional["FonctionEmployeResponse"] = None


class AttachDocumentRequest(BaseModel):
    """Demande d'attachement de document"""
    document_ids: List[int] = Field(..., description="IDs des documents à attacher")


class TaskBase(BaseSchema):
    """Schéma de base pour les tâches"""
    description_courte: str = Field(..., description="Description courte")
    description_longue: Optional[str] = Field(None, description="Description longue")
    date_echeance: Optional[datetime] = Field(None, description="Date d'échéance")


class TaskCreate(TaskBase):
    """Schéma pour créer une tâche"""
    assignee_ids: Optional[List[int]] = Field(None, description="IDs des employés assignés")


class TaskUpdate(BaseSchema):
    """Schéma pour modifier une tâche"""
    description_courte: Optional[str] = None
    description_longue: Optional[str] = None
    date_echeance: Optional[datetime] = None


class TaskResponse(TaskBase):
    """Schéma de réponse pour une tâche"""
    id_task: int
    date_creation: datetime
    assignees: Optional[List[EmployeResponse]] = None
    parent_tasks: Optional[List["TaskResponse"]] = None
    child_tasks: Optional[List["TaskResponse"]] = None


class AssignTaskRequest(BaseModel):
    """Demande d'assignation de tâche"""
    employe_id: int = Field(..., description="ID de l'employé à assigner")


class LinkSubtaskRequest(BaseModel):
    """Demande de liaison de sous-tâche"""
    child_task_id: int = Field(..., description="ID de la tâche enfant")


# Import pour éviter les références circulaires
from .referentiels import FonctionEmployeResponse
EmployeResponse.model_rebuild()
TaskResponse.model_rebuild() 