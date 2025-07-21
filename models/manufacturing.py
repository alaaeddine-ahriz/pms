"""
Modèles pour la gestion de la fabrication
"""
from sqlalchemy import Column, Text, BigInteger, ForeignKey, Numeric, DateTime, String, Table, func, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base


# Tables d'association pour la fabrication
nomenclature_produit_table = Table(
    'nomenclature_produit',
    Base.metadata,
    Column('id_nomenclature', BigInteger, ForeignKey('nomenclature_fabrication.id_nomenclature'), primary_key=True),
    Column('id_produit', BigInteger, ForeignKey('produit.id_produit'), primary_key=True),
    Column('quantite', Numeric(12, 3), nullable=False)
)

nomenclature_document_table = Table(
    'nomenclature_document',
    Base.metadata,
    Column('id_nomenclature', BigInteger, ForeignKey('nomenclature_fabrication.id_nomenclature'), primary_key=True),
    Column('id_document', BigInteger, ForeignKey('document.id_document'), primary_key=True)
)

of_nomenclature_table = Table(
    'of_nomenclature',
    Base.metadata,
    Column('id_of', BigInteger, ForeignKey('ordre_fabrication.id_of'), primary_key=True),
    Column('id_nomenclature', BigInteger, ForeignKey('nomenclature_fabrication.id_nomenclature'), primary_key=True),
    Column('quantite', Numeric(12, 3), nullable=False)
)


class NomenclatureFabrication(Base):
    """Modèle pour les nomenclatures de fabrication (BOM)"""
    __tablename__ = "nomenclature_fabrication"
    
    id_nomenclature = Column(BigInteger, primary_key=True, autoincrement=True)
    description_courte = Column(Text)
    description_longue = Column(Text)
    
    # Relations
    produits = relationship("Produit", secondary=nomenclature_produit_table)
    documents = relationship("Document", secondary=nomenclature_document_table)
    ordres_fabrication = relationship("OrdreFabrication", secondary=of_nomenclature_table, back_populates="nomenclatures")


class OrdreFabrication(Base):
    """Modèle pour les ordres de fabrication"""
    __tablename__ = "ordre_fabrication"
    
    id_of = Column(BigInteger, primary_key=True, autoincrement=True)
    date_creation = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    date_echeance = Column(DateTime(timezone=True))
    id_statut_fabrication = Column(BigInteger, ForeignKey('statut_fabrication.id_statut'))
    id_projet = Column(BigInteger, ForeignKey('projet.id_projet'))
    
    # Relations
    statut = relationship("StatutFabrication")
    projet = relationship("Projet", back_populates="ordres_fabrication")
    nomenclatures = relationship("NomenclatureFabrication", secondary=of_nomenclature_table, back_populates="ordres_fabrication")
    documents = relationship("OFDocument", back_populates="ordre_fabrication")


class OFDocument(Base):
    """Modèle pour les documents d'ordre de fabrication (photos avancement/réalisation)"""
    __tablename__ = "of_document"
    
    id_of = Column(BigInteger, ForeignKey('ordre_fabrication.id_of'), primary_key=True)
    id_document = Column(BigInteger, ForeignKey('document.id_document'), primary_key=True)
    type_photo = Column(Text, CheckConstraint("type_photo IN ('AVANCEMENT', 'REALISATION')"))
    
    # Relations
    ordre_fabrication = relationship("OrdreFabrication", back_populates="documents")
    document = relationship("Document") 