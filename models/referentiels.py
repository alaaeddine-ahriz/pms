"""
Modèles pour les données de référence
"""
from sqlalchemy import Column, String, Text, BigInteger
from database import Base


class Devise(Base):
    """Modèle pour les devises ISO-4217"""
    __tablename__ = "devise"
    
    code = Column(String(3), primary_key=True)  # ISO-4217
    libelle = Column(Text, nullable=False)


class Entreprise(Base):
    """Modèle pour les entreprises (clients, fournisseurs)"""
    __tablename__ = "entreprise"
    
    id_entreprise = Column(BigInteger, primary_key=True, autoincrement=True)
    raison_sociale = Column(Text, nullable=False)
    adresse = Column(Text)
    ice = Column(String(20))  # Identifiant Commun de l'Entreprise


class FonctionEmploye(Base):
    """Modèle pour les fonctions des employés"""
    __tablename__ = "fonction_employe"
    
    id_fonction = Column(BigInteger, primary_key=True, autoincrement=True)
    libelle = Column(Text, nullable=False)
    description = Column(Text)


class ExpenseCategory(Base):
    """Modèle pour les catégories de dépenses"""
    __tablename__ = "expense_category"
    
    id_cat = Column(BigInteger, primary_key=True, autoincrement=True)
    libelle = Column(Text, unique=True, nullable=False)


class TagDocument(Base):
    """Modèle pour les tags de documents"""
    __tablename__ = "tag_document"
    
    id_tag = Column(BigInteger, primary_key=True, autoincrement=True)
    libelle = Column(Text, unique=True, nullable=False)
    description = Column(Text)


class StatutFabrication(Base):
    """Modèle pour les statuts de fabrication"""
    __tablename__ = "statut_fabrication"
    
    id_statut = Column(BigInteger, primary_key=True, autoincrement=True)
    libelle = Column(Text, unique=True, nullable=False)


class StatutLivraison(Base):
    """Modèle pour les statuts de livraison"""
    __tablename__ = "statut_livraison"
    
    id_statut = Column(BigInteger, primary_key=True, autoincrement=True)
    libelle = Column(Text, unique=True, nullable=False)


class StatutAppro(Base):
    """Modèle pour les statuts d'approvisionnement"""
    __tablename__ = "statut_appro"
    
    id_statut = Column(BigInteger, primary_key=True, autoincrement=True)
    libelle = Column(Text, unique=True, nullable=False) 