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
    # TODO: Récupérer l'utilisateur depuis la base de données
    # Pour l'instant, on utilise des credentials de test
    if login_data.email == "admin@example.com" and login_data.password == "password123":
        # Créer le token JWT
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": "1"},  # TODO: utiliser l'ID réel de l'utilisateur
            expires_delta=access_token_expires
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
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
    # TODO: Vérifier les permissions admin
    # TODO: Vérifier que l'email n'existe pas déjà
    # TODO: Créer l'utilisateur en base
    
    # Hasher le mot de passe
    hashed_password = get_password_hash(user_data.password)
    
    # Pour l'instant, on simule la création
    return ResponseMessage(
        message=f"User {user_data.email} created successfully",
        success=True
    ) 