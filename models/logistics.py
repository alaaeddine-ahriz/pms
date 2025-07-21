"""
Modèles pour la logistique et les approvisionnements
"""
from sqlalchemy import Column, Text, BigInteger, ForeignKey, DateTime, Numeric, Table, func
from sqlalchemy.orm import relationship
from database import Base


# Tables d'association pour les demandes d'approvisionnement
supply_request_product_table = Table(
    'supply_request_product',
    Base.metadata,
    Column('id_supply_request', BigInteger, ForeignKey('supply_request.id_supply_request'), primary_key=True),
    Column('id_produit', BigInteger, ForeignKey('produit.id_produit'), primary_key=True),
    Column('quantite', Numeric(12, 3), nullable=False)
)


class Livraison(Base):
    """Modèle pour les livraisons"""
    __tablename__ = "livraison"
    
    id_livraison = Column(BigInteger, primary_key=True, autoincrement=True)
    id_move_out = Column(BigInteger, ForeignKey('stock_move.id_move'))
    id_move_in = Column(BigInteger, ForeignKey('stock_move.id_move'))
    date_livraison = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    id_statut_livraison = Column(BigInteger, ForeignKey('statut_livraison.id_statut'))
    id_livreur = Column(BigInteger, ForeignKey('employe.id_employe'))
    
    # Relations
    move_out = relationship("StockMove", foreign_keys=[id_move_out])
    move_in = relationship("StockMove", foreign_keys=[id_move_in])
    statut = relationship("StatutLivraison")
    livreur = relationship("Employe")


class SupplyRequest(Base):
    """Modèle pour les demandes d'approvisionnement"""
    __tablename__ = "supply_request"
    
    id_supply_request = Column(BigInteger, primary_key=True, autoincrement=True)
    description = Column(Text)
    date_creation = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    id_statut_appro = Column(BigInteger, ForeignKey('statut_appro.id_statut'))
    id_demandeur = Column(BigInteger, ForeignKey('employe.id_employe'))
    
    # Relations
    statut = relationship("StatutAppro")
    demandeur = relationship("Employe")
    produits = relationship("Produit", secondary=supply_request_product_table)
    tracking_events = relationship("SupplyRequestTracking", back_populates="supply_request")


class SupplyRequestTracking(Base):
    """Modèle pour le suivi des demandes d'approvisionnement"""
    __tablename__ = "supply_request_tracking"
    
    id_tracking = Column(BigInteger, primary_key=True, autoincrement=True)
    id_supply_request = Column(BigInteger, ForeignKey('supply_request.id_supply_request'), nullable=False)
    id_statut = Column(BigInteger, ForeignKey('statut_appro.id_statut'), nullable=False)
    comment = Column(Text)
    date_event = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    # Relations
    supply_request = relationship("SupplyRequest", back_populates="tracking_events")
    statut = relationship("StatutAppro") 