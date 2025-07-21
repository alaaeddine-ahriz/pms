"""
Modèles pour la gestion financière
"""
from sqlalchemy import Column, Text, BigInteger, ForeignKey, Numeric, DateTime, String, func, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base


class Account(Base):
    """Modèle pour les comptes du grand livre"""
    __tablename__ = "account"
    
    id_account = Column(BigInteger, primary_key=True, autoincrement=True)
    libelle = Column(Text, nullable=False)
    account_type = Column(Text, nullable=False, 
                         default=CheckConstraint("account_type IN ('ASSET','LIABILITY','EXPENSE','INCOME','EQUITY')"))
    
    # Relations
    debit_lines = relationship("LedgerLine", foreign_keys="LedgerLine.debit_account", back_populates="debit_account_ref")
    credit_lines = relationship("LedgerLine", foreign_keys="LedgerLine.credit_account", back_populates="credit_account_ref")
    caisse_projet = relationship("CaisseProjet", back_populates="account", uselist=False)


class LedgerLine(Base):
    """Modèle pour les lignes du grand livre (double-entrée)"""
    __tablename__ = "ledger_line"
    
    id_line = Column(BigInteger, primary_key=True, autoincrement=True)
    debit_account = Column(BigInteger, ForeignKey('account.id_account'), nullable=False)
    credit_account = Column(BigInteger, ForeignKey('account.id_account'), nullable=False)
    amount_minor = Column(BigInteger, nullable=False)  # CHECK amount_minor > 0 dans le SQL
    currency = Column(String(3), ForeignKey('devise.code'), nullable=False)
    fx_rate = Column(Numeric(16, 8))
    date_op = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    id_cat = Column(BigInteger, ForeignKey('expense_category.id_cat'))
    memo = Column(Text)
    
    # Relations
    debit_account_ref = relationship("Account", foreign_keys=[debit_account], back_populates="debit_lines")
    credit_account_ref = relationship("Account", foreign_keys=[credit_account], back_populates="credit_lines")
    devise = relationship("Devise")
    category = relationship("ExpenseCategory")
    expense_receipt = relationship("ExpenseReceipt", back_populates="ledger_line", uselist=False)


class CaisseProjet(Base):
    """Modèle pour les caisses de projet"""
    __tablename__ = "caisse_projet"
    
    id_caisse = Column(BigInteger, primary_key=True, autoincrement=True)
    id_projet = Column(BigInteger, ForeignKey('projet.id_projet'), unique=True, nullable=False)
    id_account = Column(BigInteger, ForeignKey('account.id_account'), unique=True, nullable=False)
    id_responsable = Column(BigInteger, ForeignKey('employe.id_employe'))
    
    # Relations
    projet = relationship("Projet", back_populates="caisse")
    account = relationship("Account", back_populates="caisse_projet")
    responsable = relationship("Employe")


class ExpenseReceipt(Base):
    """Modèle pour les reçus de dépenses"""
    __tablename__ = "expense_receipt"
    
    id_line = Column(BigInteger, ForeignKey('ledger_line.id_line'), primary_key=True)
    id_document = Column(BigInteger, ForeignKey('document.id_document'), nullable=False)
    
    # Relations
    ledger_line = relationship("LedgerLine", back_populates="expense_receipt")
    document = relationship("Document") 