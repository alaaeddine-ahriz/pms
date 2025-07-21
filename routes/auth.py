"""
Routes pour l'authentification
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from database import get_db
from auth import verify_password, create_access_token, get_password_hash
from schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest, CreateUserRequest
from schemas.common import ResponseMessage
from config import settings
from models.hr import Employe

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Connexion avec email et mot de passe
    Retourne un token JWT d'accès
    """
    # Récupérer l'utilisateur depuis la base de données
    user = db.query(Employe).filter(
        Employe.email == login_data.email,
        Employe.is_active == "1"
    ).first()
    
    if not user or not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Vérifier le mot de passe
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Créer le token JWT
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={
            "sub": str(user.id_employe),
            "email": user.email,
            "role": user.role
        },
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Renouvellement du token d'accès
    """
    # TODO: Implémenter la logique de renouvellement
    # Pour l'instant, on retourne une erreur
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Token refresh not implemented yet"
    )


@router.post("/register", response_model=ResponseMessage, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: CreateUserRequest,
    db: Session = Depends(get_db)
):
    """
    Création d'un nouvel utilisateur (admin seulement)
    """
    # Vérifier que l'email n'existe pas déjà
    existing_user = db.query(Employe).filter(Employe.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hasher le mot de passe
    hashed_password = get_password_hash(user_data.password)
    
    # Créer l'utilisateur
    new_user = Employe(
        nom=user_data.nom,
        prenom=user_data.prenom,
        email=user_data.email,
        password_hash=hashed_password,
        role=user_data.role,
        id_fonction=user_data.id_fonction,
        is_active="1"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return ResponseMessage(
        message=f"User {user_data.email} created successfully",
        success=True
    ) 