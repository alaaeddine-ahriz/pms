"""
Modèles pour les ressources humaines
"""
from sqlalchemy import Column, String, Text, BigInteger, DateTime, ForeignKey, Date, Numeric, Table
from sqlalchemy.orm import relationship
from database import Base
from .base import TimestampMixin


# Tables d'association
task_assignment_table = Table(
    'task_assignment',
    Base.metadata,
    Column('id_task', BigInteger, ForeignKey('task.id_task'), primary_key=True),
    Column('id_employe', BigInteger, ForeignKey('employe.id_employe'), primary_key=True)
)

task_dependency_table = Table(
    'task_dependency',
    Base.metadata,
    Column('id_parent_task', BigInteger, ForeignKey('task.id_task'), primary_key=True),
    Column('id_child_task', BigInteger, ForeignKey('task.id_task'), primary_key=True)
)

task_document_table = Table(
    'task_document',
    Base.metadata,
    Column('id_task', BigInteger, ForeignKey('task.id_task'), primary_key=True),
    Column('id_document', BigInteger, ForeignKey('document.id_document'), primary_key=True)
)


class Employe(Base, TimestampMixin):
    """Modèle pour les employés"""
    __tablename__ = "employe"
    
    id_employe = Column(BigInteger, primary_key=True, autoincrement=True)
    cin_numero = Column(String(20), unique=True)
    id_doc_cin = Column(BigInteger, ForeignKey('document.id_document'))
    nom = Column(Text, nullable=False)
    prenom = Column(Text, nullable=False)
    etat_civil = Column(Text)
    id_doc_permis = Column(BigInteger, ForeignKey('document.id_document'))
    date_naissance = Column(Date)
    salaire_net = Column(Numeric(12, 2))
    id_fonction = Column(BigInteger, ForeignKey('fonction_employe.id_fonction'))
    
    # Relations
    fonction = relationship("FonctionEmploye")
    doc_cin = relationship("Document", foreign_keys=[id_doc_cin])
    doc_permis = relationship("Document", foreign_keys=[id_doc_permis])
    uploaded_documents = relationship("Document", back_populates="uploader", foreign_keys="Document.uploaded_by")
    assigned_tasks = relationship("Task", secondary=task_assignment_table, back_populates="assignees")
    managed_projects = relationship("Projet", back_populates="chef_chantier")
    vehicle_assignments = relationship("VoitureConducteur", back_populates="employe")


class Task(Base):
    """Modèle pour les tâches"""
    __tablename__ = "task"
    
    id_task = Column(BigInteger, primary_key=True, autoincrement=True)
    description_courte = Column(Text, nullable=False)
    description_longue = Column(Text)
    date_creation = Column(DateTime(timezone=True), nullable=False, server_default="now()")
    date_echeance = Column(DateTime(timezone=True))
    
    # Relations
    assignees = relationship("Employe", secondary=task_assignment_table, back_populates="assigned_tasks")
    parent_tasks = relationship("Task", 
                               secondary=task_dependency_table,
                               primaryjoin="Task.id_task == task_dependency.c.id_child_task",
                               secondaryjoin="Task.id_task == task_dependency.c.id_parent_task",
                               back_populates="child_tasks")
    child_tasks = relationship("Task", 
                              secondary=task_dependency_table,
                              primaryjoin="Task.id_task == task_dependency.c.id_parent_task",
                              secondaryjoin="Task.id_task == task_dependency.c.id_child_task",
                              back_populates="parent_tasks")
    documents = relationship("Document", secondary=task_document_table) 