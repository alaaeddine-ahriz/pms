"""
Modèles pour la gestion du matériel
"""
from sqlalchemy import Column, BigInteger, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base


# Table d'association pour les documents de matériel
materiel_document_table = Table(
    'materiel_document',
    Base.metadata,
    Column('id_materiel', BigInteger, ForeignKey('materiel.id_materiel'), primary_key=True),
    Column('id_document', BigInteger, ForeignKey('document.id_document'), primary_key=True)
)


class Materiel(Base):
    """Modèle pour le matériel"""
    __tablename__ = "materiel"
    
    id_materiel = Column(BigInteger, primary_key=True, autoincrement=True)
    id_facture = Column(BigInteger, ForeignKey('document.id_document'))
    
    # Relations
    facture = relationship("Document", foreign_keys=[id_facture])
    documents = relationship("Document", secondary=materiel_document_table)
    projets = relationship("Projet", secondary="projet_materiel", back_populates="materiel") 