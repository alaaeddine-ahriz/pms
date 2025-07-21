"""
Schémas pour les données de référence
"""
from typing import Optional
from pydantic import BaseModel, Field
from .common import BaseSchema


class DeviseBase(BaseSchema):
    """Schéma de base pour les devises"""
    code: str = Field(..., max_length=3, description="Code ISO-4217")
    libelle: str = Field(..., description="Libellé de la devise")


class DeviseCreate(DeviseBase):
    """Schéma pour créer une devise"""
    pass


class DeviseResponse(DeviseBase):
    """Schéma de réponse pour une devise"""
    pass


class EntrepriseBase(BaseSchema):
    """Schéma de base pour les entreprises"""
    raison_sociale: str = Field(..., description="Raison sociale")
    adresse: Optional[str] = Field(None, description="Adresse")
    ice: Optional[str] = Field(None, max_length=20, description="ICE")


class EntrepriseCreate(EntrepriseBase):
    """Schéma pour créer une entreprise"""
    pass


class EntrepriseUpdate(BaseSchema):
    """Schéma pour modifier une entreprise"""
    raison_sociale: Optional[str] = None
    adresse: Optional[str] = None
    ice: Optional[str] = None


class EntrepriseResponse(EntrepriseBase):
    """Schéma de réponse pour une entreprise"""
    id_entreprise: int


class FonctionEmployeBase(BaseSchema):
    """Schéma de base pour les fonctions d'employé"""
    libelle: str = Field(..., description="Libellé de la fonction")
    description: Optional[str] = Field(None, description="Description")


class FonctionEmployeCreate(FonctionEmployeBase):
    """Schéma pour créer une fonction"""
    pass


class FonctionEmployeResponse(FonctionEmployeBase):
    """Schéma de réponse pour une fonction"""
    id_fonction: int


class ExpenseCategoryBase(BaseSchema):
    """Schéma de base pour les catégories de dépenses"""
    libelle: str = Field(..., description="Libellé de la catégorie")


class ExpenseCategoryCreate(ExpenseCategoryBase):
    """Schéma pour créer une catégorie de dépense"""
    pass


class ExpenseCategoryResponse(ExpenseCategoryBase):
    """Schéma de réponse pour une catégorie de dépense"""
    id_cat: int


class TagDocumentBase(BaseSchema):
    """Schéma de base pour les tags de documents"""
    libelle: str = Field(..., description="Libellé du tag")
    description: Optional[str] = Field(None, description="Description")


class TagDocumentCreate(TagDocumentBase):
    """Schéma pour créer un tag"""
    pass


class TagDocumentResponse(TagDocumentBase):
    """Schéma de réponse pour un tag"""
    id_tag: int


class StatutBase(BaseSchema):
    """Schéma de base pour les statuts"""
    libelle: str = Field(..., description="Libellé du statut")


class StatutCreate(StatutBase):
    """Schéma pour créer un statut"""
    pass


class StatutResponse(StatutBase):
    """Schéma de réponse pour un statut"""
    id_statut: int


# Alias pour les différents types de statuts
StatutFabricationCreate = StatutCreate
StatutFabricationResponse = StatutResponse
StatutLivraisonCreate = StatutCreate
StatutLivraisonResponse = StatutResponse
StatutApproCreate = StatutCreate
StatutApproResponse = StatutResponse 