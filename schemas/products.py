"""
Schémas pour les produits et la gestion du stock
"""
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from .common import BaseSchema


class ProduitBase(BaseSchema):
    """Schéma de base pour les produits"""
    code_produit: Optional[str] = Field(None, description="Code produit")
    libelle: Optional[str] = Field(None, description="Libellé")
    description: Optional[str] = Field(None, description="Description")


class ProduitCreate(ProduitBase):
    """Schéma pour créer un produit"""
    pass


class ProduitUpdate(BaseSchema):
    """Schéma pour modifier un produit"""
    code_produit: Optional[str] = None
    libelle: Optional[str] = None
    description: Optional[str] = None


class ProduitResponse(ProduitBase):
    """Schéma de réponse pour un produit"""
    id_produit: int
    fournisseurs: Optional[List["EntrepriseResponse"]] = None


class AddSupplierRequest(BaseModel):
    """Demande d'ajout de fournisseur"""
    entreprise_id: int = Field(..., description="ID de l'entreprise fournisseur")


class ArticleBase(BaseSchema):
    """Schéma de base pour les articles"""
    id_produit: int = Field(..., description="ID du produit")


class ArticleCreate(ArticleBase):
    """Schéma pour créer un article"""
    pass


class ArticleResponse(ArticleBase):
    """Schéma de réponse pour un article"""
    id_article: int
    produit: Optional[ProduitResponse] = None


class StockBase(BaseSchema):
    """Schéma de base pour les stocks"""
    libelle: Optional[str] = Field(None, description="Libellé du stock")
    adresse: Optional[str] = Field(None, description="Adresse")


class StockCreate(StockBase):
    """Schéma pour créer un stock"""
    pass


class StockResponse(StockBase):
    """Schéma de réponse pour un stock"""
    id_stock: int


class StockMoveBase(BaseSchema):
    """Schéma de base pour les mouvements de stock"""
    id_article: int = Field(..., description="ID de l'article")
    src_stock: Optional[int] = Field(None, description="Stock source (NULL = entrée externe)")
    dst_stock: Optional[int] = Field(None, description="Stock destination (NULL = sortie externe)")
    qty: Decimal = Field(..., gt=0, description="Quantité")
    unit_cost: Optional[Decimal] = Field(None, description="Coût unitaire")
    currency: Optional[str] = Field(None, max_length=3, description="Devise")
    ref_document: Optional[int] = Field(None, description="Document de référence")


class StockMoveCreate(StockMoveBase):
    """Schéma pour créer un mouvement de stock"""
    pass


class StockMoveResponse(StockMoveBase):
    """Schéma de réponse pour un mouvement de stock"""
    id_move: int
    date_move: datetime
    article: Optional[ArticleResponse] = None
    source_stock: Optional[StockResponse] = None
    destination_stock: Optional[StockResponse] = None


class StockInventoryResponse(BaseModel):
    """Réponse pour l'inventaire d'un stock"""
    id_stock: int
    id_article: int
    qty_available: Decimal
    article: Optional[ArticleResponse] = None
    stock: Optional[StockResponse] = None


# Import pour éviter les références circulaires
from .referentiels import EntrepriseResponse
ProduitResponse.model_rebuild() 