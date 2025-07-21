"""
Schémas pour la gestion de la fabrication
"""
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from .common import BaseSchema


class NomenclatureFabricationBase(BaseSchema):
    """Schéma de base pour les nomenclatures de fabrication"""
    description_courte: Optional[str] = Field(None, description="Description courte")
    description_longue: Optional[str] = Field(None, description="Description longue")


class NomenclatureFabricationCreate(NomenclatureFabricationBase):
    """Schéma pour créer une nomenclature"""
    pass


class NomenclatureFabricationUpdate(BaseSchema):
    """Schéma pour modifier une nomenclature"""
    description_courte: Optional[str] = None
    description_longue: Optional[str] = None


class NomenclatureFabricationResponse(NomenclatureFabricationBase):
    """Schéma de réponse pour une nomenclature"""
    id_nomenclature: int
    produits: Optional[List["ProduitResponse"]] = None


class AddBOMProductRequest(BaseModel):
    """Demande d'ajout de produit à une nomenclature"""
    product_id: int = Field(..., description="ID du produit")
    qty: Decimal = Field(..., gt=0, description="Quantité")


class OrdreFabricationBase(BaseSchema):
    """Schéma de base pour les ordres de fabrication"""
    date_echeance: Optional[datetime] = Field(None, description="Date d'échéance")
    id_statut_fabrication: Optional[int] = Field(None, description="ID statut")
    id_projet: Optional[int] = Field(None, description="ID projet")


class OrdreFabricationCreate(OrdreFabricationBase):
    """Schéma pour créer un ordre de fabrication"""
    pass


class OrdreFabricationUpdate(BaseSchema):
    """Schéma pour modifier un ordre de fabrication"""
    date_echeance: Optional[datetime] = None
    id_statut_fabrication: Optional[int] = None
    id_projet: Optional[int] = None


class OrdreFabricationResponse(OrdreFabricationBase):
    """Schéma de réponse pour un ordre de fabrication"""
    id_of: int
    date_creation: datetime
    statut: Optional["StatutFabricationResponse"] = None
    projet: Optional["ProjetResponse"] = None
    nomenclatures: Optional[List[NomenclatureFabricationResponse]] = None


class LinkBOMRequest(BaseModel):
    """Demande de liaison de nomenclature"""
    nomenclature_id: int = Field(..., description="ID de la nomenclature")
    qty: Decimal = Field(..., gt=0, description="Quantité")


class UpdateStatusRequest(BaseModel):
    """Demande de mise à jour de statut"""
    status_id: int = Field(..., description="ID du nouveau statut")


class OFDocumentResponse(BaseSchema):
    """Réponse pour un document d'ordre de fabrication"""
    id_of: int
    id_document: int
    type_photo: Optional[str] = None
    document: Optional["DocumentResponse"] = None


# Import pour éviter les références circulaires
from .products import ProduitResponse
from .referentiels import StatutFabricationResponse
from .projects import ProjetResponse
from .documents import DocumentResponse

NomenclatureFabricationResponse.model_rebuild()
OrdreFabricationResponse.model_rebuild()
OFDocumentResponse.model_rebuild() 