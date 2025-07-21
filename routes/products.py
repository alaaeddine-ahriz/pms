"""
Routes pour la gestion des produits et du stock
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from dependencies import get_pagination_params, require_authenticated_user
from schemas.common import PaginationParams, ResponseMessage
from schemas.products import *
from models.products import Produit, Article, Stock, StockMove
from models.referentiels import Entreprise

router = APIRouter(prefix="/api/v1", tags=["Products & Stock"])


# ======================= PRODUITS ==========================

@router.get("/products", response_model=List[ProduitResponse])
async def list_products(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des produits avec pagination"""
    skip = (pagination.page - 1) * pagination.page_size
    products = db.query(Produit).offset(skip).limit(pagination.page_size).all()
    return products


@router.post("/products", response_model=ProduitResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProduitCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer un nouveau produit"""
    # Vérifier que le code produit n'existe pas déjà
    if product_data.code_produit:
        existing = db.query(Produit).filter(Produit.code_produit == product_data.code_produit).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with code {product_data.code_produit} already exists"
            )
    
    product = Produit(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/products/{product_id}", response_model=ProduitResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer un produit par ID"""
    product = db.query(Produit).filter(Produit.id_produit == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.patch("/products/{product_id}", response_model=ProduitResponse)
async def update_product(
    product_id: int,
    product_data: ProduitUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Modifier un produit"""
    product = db.query(Produit).filter(Produit.id_produit == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Mettre à jour uniquement les champs fournis
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    return product


@router.post("/products/{product_id}/suppliers", response_model=ResponseMessage)
async def add_product_supplier(
    product_id: int,
    supplier_request: AddSupplierRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Ajouter un fournisseur à un produit"""
    product = db.query(Produit).filter(Produit.id_produit == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    supplier = db.query(Entreprise).filter(Entreprise.id_entreprise == supplier_request.entreprise_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    
    # Ajouter le fournisseur s'il n'est pas déjà associé
    if supplier not in product.fournisseurs:
        product.fournisseurs.append(supplier)
        db.commit()
    
    return ResponseMessage(
        message=f"Supplier {supplier_request.entreprise_id} added to product {product_id}",
        success=True
    )


@router.delete("/products/{product_id}/suppliers/{supplier_id}", response_model=ResponseMessage)
async def remove_product_supplier(
    product_id: int,
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Retirer un fournisseur d'un produit"""
    product = db.query(Produit).filter(Produit.id_produit == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    supplier = db.query(Entreprise).filter(Entreprise.id_entreprise == supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    
    if supplier in product.fournisseurs:
        product.fournisseurs.remove(supplier)
        db.commit()
    
    return ResponseMessage(
        message=f"Supplier {supplier_id} removed from product {product_id}",
        success=True
    )


# ======================= ARTICLES (SKU) ==========================

@router.get("/articles", response_model=List[ArticleResponse])
async def list_articles(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des articles (SKU) avec pagination"""
    skip = (pagination.page - 1) * pagination.page_size
    articles = db.query(Article).offset(skip).limit(pagination.page_size).all()
    return articles


@router.post("/articles", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    article_data: ArticleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer un nouvel article (SKU)"""
    # Vérifier que le produit existe
    product = db.query(Produit).filter(Produit.id_produit == article_data.id_produit).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product not found"
        )
    
    article = Article(**article_data.model_dump())
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


@router.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer un article par ID"""
    article = db.query(Article).filter(Article.id_article == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    return article


# ======================= STOCKS ==========================

@router.get("/stocks", response_model=List[StockResponse])
async def list_stocks(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Liste des stocks/entrepôts avec pagination"""
    skip = (pagination.page - 1) * pagination.page_size
    stocks = db.query(Stock).offset(skip).limit(pagination.page_size).all()
    return stocks


@router.post("/stocks", response_model=StockResponse, status_code=status.HTTP_201_CREATED)
async def create_stock(
    stock_data: StockCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer un nouveau stock/entrepôt"""
    stock = Stock(**stock_data.model_dump())
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock


@router.get("/stocks/{stock_id}", response_model=StockResponse)
async def get_stock(
    stock_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer un stock par ID"""
    stock = db.query(Stock).filter(Stock.id_stock == stock_id).first()
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock not found"
        )
    return stock


@router.get("/stocks/{stock_id}/inventory", response_model=List[StockInventoryResponse])
async def get_stock_inventory(
    stock_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer l'inventaire actuel d'un stock"""
    # Vérifier que le stock existe
    stock = db.query(Stock).filter(Stock.id_stock == stock_id).first()
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock not found"
        )
    
    # Requête pour calculer les quantités disponibles
    # Note: En production, utiliser la vue matérialisée stock_inventory
    query = text("""
        SELECT 
            :stock_id as id_stock,
            sm.id_article,
            SUM(
                CASE 
                    WHEN sm.dst_stock = :stock_id THEN sm.qty
                    WHEN sm.src_stock = :stock_id THEN -sm.qty
                    ELSE 0
                END
            ) as qty_available
        FROM stock_move sm
        WHERE (sm.dst_stock = :stock_id OR sm.src_stock = :stock_id)
        GROUP BY sm.id_article
        HAVING SUM(
            CASE 
                WHEN sm.dst_stock = :stock_id THEN sm.qty
                WHEN sm.src_stock = :stock_id THEN -sm.qty
                ELSE 0
            END
        ) > 0
    """)
    
    result = db.execute(query, {"stock_id": stock_id})
    inventory_data = []
    
    for row in result:
        inventory_data.append(StockInventoryResponse(
            id_stock=row.id_stock,
            id_article=row.id_article,
            qty_available=row.qty_available
        ))
    
    return inventory_data


# ======================= MOUVEMENTS DE STOCK ==========================

@router.post("/stock-moves", response_model=StockMoveResponse, status_code=status.HTTP_201_CREATED)
async def create_stock_move(
    move_data: StockMoveCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Créer un mouvement de stock (double-entrée)"""
    # Vérifier que l'article existe
    article = db.query(Article).filter(Article.id_article == move_data.id_article).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article not found"
        )
    
    # Vérifier que les stocks existent
    if move_data.src_stock:
        src_stock = db.query(Stock).filter(Stock.id_stock == move_data.src_stock).first()
        if not src_stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Source stock not found"
            )
    
    if move_data.dst_stock:
        dst_stock = db.query(Stock).filter(Stock.id_stock == move_data.dst_stock).first()
        if not dst_stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Destination stock not found"
            )
    
    # Vérifier qu'au moins un stock est spécifié
    if not move_data.src_stock and not move_data.dst_stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one stock (source or destination) must be specified"
        )
    
    stock_move = StockMove(**move_data.model_dump())
    db.add(stock_move)
    db.commit()
    db.refresh(stock_move)
    return stock_move


@router.get("/stock-moves/{move_id}", response_model=StockMoveResponse)
async def get_stock_move(
    move_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """Récupérer un mouvement de stock par ID"""
    move = db.query(StockMove).filter(StockMove.id_move == move_id).first()
    if not move:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock move not found"
        )
    return move 