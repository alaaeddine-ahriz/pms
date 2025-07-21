"""
Schémas pour la gestion du matériel
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from .common import BaseSchema


class MaterielBase(BaseSchema):
    """Schéma de base pour le matériel"""
    id_facture: Optional[int] = Field(None, description="ID document facture")


class MaterielCreate(MaterielBase):
    """Schéma pour créer du matériel"""
    pass


class MaterielUpdate(BaseSchema):
    """Schéma pour modifier du matériel"""
    id_facture: Optional[int] = None


class MaterielResponse(MaterielBase):
    """Schéma de réponse pour le matériel"""
    id_materiel: int
    documents: Optional[List["DocumentResponse"]] = None





# Import pour éviter les références circulaires
from .documents import DocumentResponse
MaterielResponse.model_rebuild() 