"""
Modèles pour la gestion des produits et du stock
"""
from sqlalchemy import Column, String, Text, BigInteger, ForeignKey, Numeric, DateTime, Table, func
from sqlalchemy.orm import relationship
from database import Base


# Table d'association pour les fournisseurs de produits
produit_fournisseur_table = Table(
    'produit_fournisseur',
    Base.metadata,
    Column('id_produit', BigInteger, ForeignKey('produit.id_produit'), primary_key=True),
    Column('id_entreprise', BigInteger, ForeignKey('entreprise.id_entreprise'), primary_key=True)
)


class Produit(Base):
    """Modèle pour les produits (références)"""
    __tablename__ = "produit"
    
    id_produit = Column(BigInteger, primary_key=True, autoincrement=True)
    code_produit = Column(Text, unique=True)
    libelle = Column(Text)
    description = Column(Text)
    
    # Relations
    fournisseurs = relationship("Entreprise", secondary=produit_fournisseur_table)
    articles = relationship("Article", back_populates="produit")


class Article(Base):
    """Modèle pour les articles (SKU)"""
    __tablename__ = "article"
    
    id_article = Column(BigInteger, primary_key=True, autoincrement=True)
    id_produit = Column(BigInteger, ForeignKey('produit.id_produit'))
    
    # Relations
    produit = relationship("Produit", back_populates="articles")
    stock_moves = relationship("StockMove", back_populates="article")


class Stock(Base):
    """Modèle pour les dépôts/entrepôts"""
    __tablename__ = "stock"
    
    id_stock = Column(BigInteger, primary_key=True, autoincrement=True)
    libelle = Column(Text)
    adresse = Column(Text)
    
    # Relations
    moves_out = relationship("StockMove", foreign_keys="StockMove.src_stock", back_populates="source_stock")
    moves_in = relationship("StockMove", foreign_keys="StockMove.dst_stock", back_populates="destination_stock")


class StockMove(Base):
    """Modèle pour les mouvements de stock (double-entrée)"""
    __tablename__ = "stock_move"
    
    id_move = Column(BigInteger, primary_key=True, autoincrement=True)
    id_article = Column(BigInteger, ForeignKey('article.id_article'), nullable=False)
    src_stock = Column(BigInteger, ForeignKey('stock.id_stock'))  # NULL = entrée externe
    dst_stock = Column(BigInteger, ForeignKey('stock.id_stock'))  # NULL = sortie externe
    qty = Column(Numeric(12, 3), nullable=False)  # CHECK qty > 0 dans le SQL
    unit_cost = Column(Numeric(14, 4))
    currency = Column(String(3), ForeignKey('devise.code'))
    date_move = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    ref_document = Column(BigInteger, ForeignKey('document.id_document'))
    
    # Relations
    article = relationship("Article", back_populates="stock_moves")
    source_stock = relationship("Stock", foreign_keys=[src_stock], back_populates="moves_out")
    destination_stock = relationship("Stock", foreign_keys=[dst_stock], back_populates="moves_in")
    devise = relationship("Devise")
    document = relationship("Document") 