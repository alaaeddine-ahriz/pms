"""
Schémas pour la logistique et les approvisionnements
"""
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from .common import BaseSchema


class LivraisonBase(BaseSchema):
    """Schéma de base pour les livraisons"""
    id_move_out: Optional[int] = Field(None, description="ID mouvement de sortie")
    id_move_in: Optional[int] = Field(None, description="ID mouvement d'entrée")
    id_statut_livraison: Optional[int] = Field(None, description="ID statut livraison")
    id_livreur: Optional[int] = Field(None, description="ID livreur")


class LivraisonCreate(LivraisonBase):
    """Schéma pour créer une livraison"""
    pass


class LivraisonUpdate(BaseSchema):
    """Schéma pour modifier une livraison"""
    id_statut_livraison: Optional[int] = None
    id_livreur: Optional[int] = None


class LivraisonResponse(LivraisonBase):
    """Schéma de réponse pour une livraison"""
    id_livraison: int
    date_livraison: datetime
    statut: Optional["StatutLivraisonResponse"] = None
    livreur: Optional["EmployeResponse"] = None
    move_out: Optional["StockMoveResponse"] = None
    move_in: Optional["StockMoveResponse"] = None


class UpdateDeliveryStatusRequest(BaseModel):
    """Demande de mise à jour de statut de livraison"""
    status_id: int = Field(..., description="ID du nouveau statut")


class SupplyRequestBase(BaseSchema):
    """Schéma de base pour les demandes d'approvisionnement"""
    description: Optional[str] = Field(None, description="Description")
    id_statut_appro: Optional[int] = Field(None, description="ID statut")
    id_demandeur: Optional[int] = Field(None, description="ID demandeur")


class SupplyRequestCreate(SupplyRequestBase):
    """Schéma pour créer une demande d'approvisionnement"""
    pass


class SupplyRequestUpdate(BaseSchema):
    """Schéma pour modifier une demande d'approvisionnement"""
    description: Optional[str] = None
    id_statut_appro: Optional[int] = None


class SupplyRequestResponse(SupplyRequestBase):
    """Schéma de réponse pour une demande d'approvisionnement"""
    id_supply_request: int
    date_creation: datetime
    statut: Optional["StatutApproResponse"] = None
    demandeur: Optional["EmployeResponse"] = None
    produits: Optional[List["ProduitResponse"]] = None
    tracking_events: Optional[List["SupplyRequestTrackingResponse"]] = None


class AddSupplyProductRequest(BaseModel):
    """Demande d'ajout de produit à une demande d'approvisionnement"""
    product_id: int = Field(..., description="ID du produit")
    qty: Decimal = Field(..., gt=0, description="Quantité")


class SupplyRequestTrackingBase(BaseSchema):
    """Schéma de base pour le suivi d'approvisionnement"""
    id_statut: int = Field(..., description="ID statut")
    comment: Optional[str] = Field(None, description="Commentaire")


class SupplyRequestTrackingCreate(SupplyRequestTrackingBase):
    """Schéma pour créer un événement de suivi"""
    pass


class SupplyRequestTrackingResponse(SupplyRequestTrackingBase):
    """Schéma de réponse pour un événement de suivi"""
    id_tracking: int
    id_supply_request: int
    date_event: datetime
    statut: Optional["StatutApproResponse"] = None


# Import pour éviter les références circulaires
from .referentiels import StatutLivraisonResponse, StatutApproResponse
from .hr import EmployeResponse
from .products import StockMoveResponse, ProduitResponse

LivraisonResponse.model_rebuild()
SupplyRequestResponse.model_rebuild()
SupplyRequestTrackingResponse.model_rebuild() 