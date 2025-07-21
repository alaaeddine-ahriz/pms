"""
Schémas pour la gestion des véhicules
"""
from typing import Optional, List
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field
from .common import BaseSchema, TimestampMixin


class VoitureBase(BaseSchema):
    """Schéma de base pour les véhicules"""
    immatriculation: Optional[str] = Field(None, max_length=15, description="Immatriculation")
    modele: Optional[str] = Field(None, description="Modèle")
    marque: Optional[str] = Field(None, description="Marque")


class VoitureCreate(VoitureBase):
    """Schéma pour créer un véhicule"""
    id_carte_grise: Optional[int] = Field(None, description="ID document carte grise")
    id_assurance: Optional[int] = Field(None, description="ID document assurance")


class VoitureUpdate(VoitureBase):
    """Schéma pour modifier un véhicule"""
    id_carte_grise: Optional[int] = None
    id_assurance: Optional[int] = None


class VoitureResponse(VoitureBase, TimestampMixin):
    """Schéma de réponse pour un véhicule"""
    id_voiture: int
    id_carte_grise: Optional[int] = None
    id_assurance: Optional[int] = None
    km_logs: Optional[List["VoitureKmLogResponse"]] = None
    conducteurs: Optional[List["VoitureConducteurResponse"]] = None


class VoitureKmLogBase(BaseSchema):
    """Schéma de base pour les relevés kilométriques"""
    date_releve: date = Field(..., description="Date du relevé")
    kilometrage: Decimal = Field(..., description="Kilométrage")


class VoitureKmLogCreate(VoitureKmLogBase):
    """Schéma pour créer un relevé kilométrique"""
    pass


class VoitureKmLogResponse(VoitureKmLogBase):
    """Schéma de réponse pour un relevé kilométrique"""
    id_voiture: int


class VoitureConducteurBase(BaseSchema):
    """Schéma de base pour les assignations conducteur"""
    employe_id: int = Field(..., description="ID de l'employé")
    date_start: date = Field(..., description="Date de début")


class VoitureConducteurCreate(VoitureConducteurBase):
    """Schéma pour assigner un conducteur"""
    pass


class VoitureConducteurUpdate(BaseSchema):
    """Schéma pour modifier une assignation"""
    date_end: Optional[date] = Field(None, description="Date de fin")


class VoitureConducteurResponse(VoitureConducteurBase):
    """Schéma de réponse pour une assignation conducteur"""
    id_voiture: int
    date_debut: date
    date_fin: Optional[date] = None
    employe: Optional["EmployeResponse"] = None


# Import pour éviter les références circulaires
from .hr import EmployeResponse
VoitureResponse.model_rebuild()
VoitureConducteurResponse.model_rebuild() 