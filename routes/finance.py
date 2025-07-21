"""
Routes pour la gestion financière
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_pagination_params, require_authenticated_user
from schemas.common import PaginationParams, ResponseMessage
from schemas.finance import *
from models.finance import Account, LedgerLine

router = APIRouter(prefix="/api/v1", tags=["Finance"])


# ======================= COMPTES DU GRAND LIVRE ==========================

@router.get("/ledger/accounts", response_model=List[AccountResponse])
async def list_accounts(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des comptes du grand livre (readonly sauf admin)"""
    skip = (pagination.page - 1) * pagination.page_size
    accounts = db.query(Account).offset(skip).limit(pagination.page_size).all()
    return accounts


@router.post("/ledger/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: AccountCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer un nouveau compte (admin seulement)"""
    # TODO: Vérifier les permissions admin
    
    account = Account(**account_data.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.get("/ledger/accounts/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer un compte par ID"""
    account = db.query(Account).filter(Account.id_account == account_id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    return account


# ======================= LIGNES DU GRAND LIVRE ==========================

@router.post("/ledger/lines", response_model=LedgerLineResponse, status_code=status.HTTP_201_CREATED)
async def create_ledger_line(
    line_data: LedgerLineCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer une ligne de grand livre générique (flux non-caisse)"""
    # Vérifier que les comptes existent
    debit_account = db.query(Account).filter(Account.id_account == line_data.debit_account).first()
    if not debit_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debit account not found"
        )
    
    credit_account = db.query(Account).filter(Account.id_account == line_data.credit_account).first()
    if not credit_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credit account not found"
        )
    
    # Vérifier que les comptes sont différents
    if line_data.debit_account == line_data.credit_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debit and credit accounts must be different"
        )
    
    # Vérifier la catégorie si spécifiée
    if line_data.id_cat:
        from models.referentiels import ExpenseCategory
        category = db.query(ExpenseCategory).filter(ExpenseCategory.id_cat == line_data.id_cat).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Expense category not found"
            )
    
    ledger_line = LedgerLine(**line_data.model_dump())
    db.add(ledger_line)
    db.commit()
    db.refresh(ledger_line)
    return ledger_line


@router.get("/ledger/lines/{line_id}", response_model=LedgerLineResponse)
async def get_ledger_line(
    line_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer une ligne de grand livre par ID"""
    line = db.query(LedgerLine).filter(LedgerLine.id_line == line_id).first()
    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ledger line not found"
        )
    return line


@router.get("/ledger/lines", response_model=List[LedgerLineResponse])
async def list_ledger_lines(
    pagination: PaginationParams = Depends(get_pagination_params),
    account_id: int = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des lignes de grand livre avec filtrage optionnel par compte"""
    skip = (pagination.page - 1) * pagination.page_size
    
    query = db.query(LedgerLine)
    
    # Filtrer par compte si spécifié
    if account_id:
        query = query.filter(
            (LedgerLine.debit_account == account_id) |
            (LedgerLine.credit_account == account_id)
        )
    
    lines = query.order_by(LedgerLine.date_op.desc()).offset(skip).limit(pagination.page_size).all()
    return lines


# ======================= RAPPORTS FINANCIERS ==========================

@router.get("/ledger/balance", response_model=List[dict])
async def get_trial_balance(
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Balance de vérification - soldes de tous les comptes"""
    from sqlalchemy import text
    
    query = text("""
        SELECT 
            a.id_account,
            a.libelle,
            a.account_type,
            COALESCE(SUM(
                CASE 
                    WHEN ll.debit_account = a.id_account THEN ll.amount_minor
                    WHEN ll.credit_account = a.id_account THEN -ll.amount_minor
                    ELSE 0
                END
            ), 0) as balance_minor
        FROM account a
        LEFT JOIN ledger_line ll ON (ll.debit_account = a.id_account OR ll.credit_account = a.id_account)
        GROUP BY a.id_account, a.libelle, a.account_type
        ORDER BY a.account_type, a.libelle
    """)
    
    result = db.execute(query)
    
    balance_data = []
    for row in result:
        balance = float(row.balance_minor) / 100  # Convertir en unités principales
        
        balance_data.append({
            "id_account": row.id_account,
            "libelle": row.libelle,
            "account_type": row.account_type,
            "balance": balance
        })
    
    return balance_data


@router.get("/ledger/profit-loss", response_model=dict)
async def get_profit_loss(
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Compte de résultat simplifié"""
    from sqlalchemy import text
    
    # Calculer les revenus (INCOME accounts)
    income_query = text("""
        SELECT COALESCE(SUM(
            CASE 
                WHEN ll.credit_account = a.id_account THEN ll.amount_minor
                WHEN ll.debit_account = a.id_account THEN -ll.amount_minor
                ELSE 0
            END
        ), 0) as total_income
        FROM account a
        LEFT JOIN ledger_line ll ON (ll.debit_account = a.id_account OR ll.credit_account = a.id_account)
        WHERE a.account_type = 'INCOME'
    """)
    
    # Calculer les dépenses (EXPENSE accounts)
    expense_query = text("""
        SELECT COALESCE(SUM(
            CASE 
                WHEN ll.debit_account = a.id_account THEN ll.amount_minor
                WHEN ll.credit_account = a.id_account THEN -ll.amount_minor
                ELSE 0
            END
        ), 0) as total_expenses
        FROM account a
        LEFT JOIN ledger_line ll ON (ll.debit_account = a.id_account OR ll.credit_account = a.id_account)
        WHERE a.account_type = 'EXPENSE'
    """)
    
    income_result = db.execute(income_query).first()
    expense_result = db.execute(expense_query).first()
    
    total_income = float(income_result.total_income) / 100
    total_expenses = float(expense_result.total_expenses) / 100
    net_profit = total_income - total_expenses
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_profit": net_profit,
        "currency": "MAD"
    } 