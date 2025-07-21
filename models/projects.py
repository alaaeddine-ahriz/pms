"""
Modèles pour la gestion des projets
"""
from sqlalchemy import Column, Text, BigInteger, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from database import Base


# Tables d'association pour les projets
projet_voiture_table = Table(
    'projet_voiture',
    Base.metadata,
    Column('id_projet', BigInteger, ForeignKey('projet.id_projet'), primary_key=True),
    Column('id_voiture', BigInteger, ForeignKey('voiture.id_voiture'), primary_key=True)
)

projet_materiel_table = Table(
    'projet_materiel',
    Base.metadata,
    Column('id_projet', BigInteger, ForeignKey('projet.id_projet'), primary_key=True),
    Column('id_materiel', BigInteger, ForeignKey('materiel.id_materiel'), primary_key=True)
)

projet_document_table = Table(
    'projet_document',
    Base.metadata,
    Column('id_projet', BigInteger, ForeignKey('projet.id_projet'), primary_key=True),
    Column('id_document', BigInteger, ForeignKey('document.id_document'), primary_key=True)
)


class SiteClient(Base):
    """Modèle pour les sites clients"""
    __tablename__ = "site_client"
    
    id_site_client = Column(BigInteger, primary_key=True, autoincrement=True)
    adresse = Column(Text)
    id_client = Column(BigInteger, ForeignKey('entreprise.id_entreprise'))
    
    # Relations
    client = relationship("Entreprise")
    projets = relationship("Projet", back_populates="site_client")


class Projet(Base):
    """Modèle pour les projets"""
    __tablename__ = "projet"
    
    id_projet = Column(BigInteger, primary_key=True, autoincrement=True)
    adresse = Column(Text)
    date_debut = Column(Date)
    id_site_client = Column(BigInteger, ForeignKey('site_client.id_site_client'))
    id_chef_chantier = Column(BigInteger, ForeignKey('employe.id_employe'))
    id_icone = Column(BigInteger, ForeignKey('document.id_document'))
    
    # Relations
    site_client = relationship("SiteClient", back_populates="projets")
    chef_chantier = relationship("Employe", back_populates="managed_projects")
    icone = relationship("Document")
    voitures = relationship("Voiture", secondary=projet_voiture_table, back_populates="projets")
    materiel = relationship("Materiel", secondary=projet_materiel_table, back_populates="projets")
    documents = relationship("Document", secondary=projet_document_table)
    caisse = relationship("CaisseProjet", back_populates="projet", uselist=False)
    ordres_fabrication = relationship("OrdreFabrication", back_populates="projet") 