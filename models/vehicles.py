"""
Modèles pour la gestion du parc de véhicules
"""
from sqlalchemy import Column, String, Text, BigInteger, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from database import Base
from .base import TimestampMixin


class Voiture(Base, TimestampMixin):
    """Modèle pour les véhicules"""
    __tablename__ = "voiture"
    
    id_voiture = Column(BigInteger, primary_key=True, autoincrement=True)
    immatriculation = Column(String(15), unique=True)
    modele = Column(Text)
    marque = Column(Text)
    id_carte_grise = Column(BigInteger, ForeignKey('document.id_document'))
    id_assurance = Column(BigInteger, ForeignKey('document.id_document'))
    
    # Relations
    carte_grise = relationship("Document", foreign_keys=[id_carte_grise])
    assurance = relationship("Document", foreign_keys=[id_assurance])
    km_logs = relationship("VoitureKmLog", back_populates="voiture")
    conducteurs = relationship("VoitureConducteur", back_populates="voiture")
    projets = relationship("Projet", secondary="projet_voiture", back_populates="voitures")


class VoitureKmLog(Base):
    """Modèle pour les relevés kilométriques"""
    __tablename__ = "voiture_km_log"
    
    id_voiture = Column(BigInteger, ForeignKey('voiture.id_voiture'), primary_key=True)
    date_releve = Column(Date, primary_key=True, nullable=False)
    kilometrage = Column(Numeric(10, 1), nullable=False)
    
    # Relations
    voiture = relationship("Voiture", back_populates="km_logs")


class VoitureConducteur(Base):
    """Modèle pour l'assignation des conducteurs aux véhicules"""
    __tablename__ = "voiture_conducteur"
    
    id_voiture = Column(BigInteger, ForeignKey('voiture.id_voiture'), primary_key=True)
    id_employe = Column(BigInteger, ForeignKey('employe.id_employe'), primary_key=True)
    date_debut = Column(Date, primary_key=True, nullable=False)
    date_fin = Column(Date)
    
    # Relations
    voiture = relationship("Voiture", back_populates="conducteurs")
    employe = relationship("Employe", back_populates="vehicle_assignments") 