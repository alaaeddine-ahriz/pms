"""
Schémas pour la gestion financière
"""
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from .common import BaseSchema


class AccountBase(BaseSchema):
    """Schéma de base pour les comptes"""
    libelle: str = Field(..., description="Libellé du compte")
    account_type: str = Field(..., description="Type de compte", 
                             regex="^(ASSET|LIABILITY|EXPENSE|INCOME|EQUITY)$")


class AccountCreate(AccountBase):
    """Schéma pour créer un compte"""
    pass


class AccountResponse(AccountBase):
    """Schéma de réponse pour un compte"""
    id_account: int


class LedgerLineBase(BaseSchema):
    """Schéma de base pour les lignes de grand livre"""
    debit_account: int = Field(..., description="Compte débiteur")
    credit_account: int = Field(..., description="Compte créditeur")
    amount_minor: int = Field(..., gt=0, description="Montant en unités mineures")
    currency: str = Field(..., max_length=3, description="Devise")
    fx_rate: Optional[Decimal] = Field(None, description="Taux de change")
    id_cat: Optional[int] = Field(None, description="ID catégorie")
    memo: Optional[str] = Field(None, description="Mémo")


class LedgerLineCreate(LedgerLineBase):
    """Schéma pour créer une ligne de grand livre"""
    pass


class LedgerLineResponse(LedgerLineBase):
    """Schéma de réponse pour une ligne de grand livre"""
    id_line: int
    date_op: datetime
    debit_account_ref: Optional[AccountResponse] = None
    credit_account_ref: Optional[AccountResponse] = None
    category: Optional["ExpenseCategoryResponse"] = None


class CaisseProjectBalance(BaseModel):
    """Réponse pour le solde d'une caisse projet"""
    id_caisse: int
    id_projet: int
    balance: Decimal
    currency: str
    last_transaction: Optional[datetime] = None


class CaisseTopUpRequest(BaseModel):
    """Demande d'alimentation de caisse"""
    amount: Decimal = Field(..., gt=0, description="Montant")
    currency: str = Field(..., max_length=3, description="Devise")
    fx_rate: Optional[Decimal] = Field(None, description="Taux de change")
    memo: Optional[str] = Field(None, description="Mémo")


class CaisseExpenseRequest(BaseModel):
    """Demande de dépense de caisse"""
    amount: Decimal = Field(..., gt=0, description="Montant")
    currency: str = Field(..., max_length=3, description="Devise")
    category_id: int = Field(..., description="ID catégorie de dépense")
    memo: Optional[str] = Field(None, description="Mémo")
    receipt_document_id: int = Field(..., description="ID document reçu")


class CaisseLedgerEntry(BaseModel):
    """Entrée du grand livre d'une caisse"""
    id_line: int
    date_op: datetime
    type: str  # 'TOP_UP' ou 'EXPENSE'
    amount: Decimal
    currency: str
    memo: Optional[str] = None
    category: Optional[str] = None
    balance_after: Decimal


# Import pour éviter les références circulaires
from .referentiels import ExpenseCategoryResponse
LedgerLineResponse.model_rebuild() 