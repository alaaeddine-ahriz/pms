"""
Schémas pour la gestion des projets
"""
from typing import Optional, List
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field
from .common import BaseSchema


class SiteClientBase(BaseSchema):
    """Schéma de base pour les sites clients"""
    adresse: Optional[str] = Field(None, description="Adresse")
    id_client: Optional[int] = Field(None, description="ID client")


class SiteClientCreate(SiteClientBase):
    """Schéma pour créer un site client"""
    pass


class SiteClientResponse(SiteClientBase):
    """Schéma de réponse pour un site client"""
    id_site_client: int
    client: Optional["EntrepriseResponse"] = None


class ProjetBase(BaseSchema):
    """Schéma de base pour les projets"""
    adresse: Optional[str] = Field(None, description="Adresse")
    date_debut: Optional[date] = Field(None, description="Date de début")
    id_site_client: Optional[int] = Field(None, description="ID site client")
    id_chef_chantier: Optional[int] = Field(None, description="ID chef de chantier")
    id_icone: Optional[int] = Field(None, description="ID icône")


class ProjetCreate(ProjetBase):
    """Schéma pour créer un projet"""
    pass


class ProjetUpdate(BaseSchema):
    """Schéma pour modifier un projet"""
    adresse: Optional[str] = None
    date_debut: Optional[date] = None
    id_site_client: Optional[int] = None
    id_chef_chantier: Optional[int] = None
    id_icone: Optional[int] = None


class ProjetResponse(ProjetBase):
    """Schéma de réponse pour un projet"""
    id_projet: int
    site_client: Optional[SiteClientResponse] = None
    chef_chantier: Optional["EmployeResponse"] = None
    voitures: Optional[List["VoitureResponse"]] = None
    materiel: Optional[List["MaterielResponse"]] = None
    caisse: Optional["CaisseProjetResponse"] = None


class LinkVehicleRequest(BaseModel):
    """Demande de liaison de véhicule"""
    vehicle_id: int = Field(..., description="ID du véhicule")


class LinkMaterialRequest(BaseModel):
    """Demande de liaison de matériel"""
    material_id: int = Field(..., description="ID du matériel")


class CaisseProjetResponse(BaseSchema):
    """Réponse pour une caisse de projet"""
    id_caisse: int
    id_projet: int
    id_account: int
    id_responsable: Optional[int]
    responsable: Optional["EmployeResponse"] = None


class CaisseBalanceResponse(BaseModel):
    """Réponse pour le solde d'une caisse"""
    balance: Decimal
    currency: str
    last_updated: Optional[str] = None


class CaisseTopUpRequest(BaseModel):
    """Demande d'alimentation de caisse"""
    amount: Decimal = Field(..., gt=0, description="Montant")
    currency: str = Field(..., max_length=3, description="Devise")
    fx_rate: Optional[Decimal] = Field(None, description="Taux de change")
    memo: Optional[str] = Field(None, description="Mémo")


class CaisseExpenseRequest(BaseModel):
    """Demande de dépense de caisse"""
    amount: Decimal = Field(..., gt=0, description="Montant")
    currency: str = Field(..., max_length=3, description="Devise")
    category_id: int = Field(..., description="ID catégorie")
    memo: Optional[str] = Field(None, description="Mémo")
    receipt_document_id: Optional[int] = Field(None, description="ID document reçu")


# Import pour éviter les références circulaires
from .referentiels import EntrepriseResponse
from .hr import EmployeResponse
from .vehicles import VoitureResponse
from .materials import MaterielResponse

SiteClientResponse.model_rebuild()
ProjetResponse.model_rebuild()
CaisseProjetResponse.model_rebuild() 