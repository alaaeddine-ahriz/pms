"""
Schémas pour l'authentification
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Demande de connexion"""
    email: EmailStr = Field(..., description="Adresse email")
    password: str = Field(..., min_length=6, description="Mot de passe")


class TokenResponse(BaseModel):
    """Réponse avec token JWT"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # en secondes


class RefreshTokenRequest(BaseModel):
    """Demande de renouvellement de token"""
    refresh_token: str


class UserInfo(BaseModel):
    """Informations utilisateur"""
    id: int
    email: str
    nom: str
    prenom: str
    fonction: Optional[str] = None
    
    class Config:
        from_attributes = True


class CreateUserRequest(BaseModel):
    """Demande de création d'utilisateur"""
    email: EmailStr
    password: str = Field(..., min_length=6)
    nom: str
    prenom: str
    id_fonction: Optional[int] = None
    role: str = Field(..., description="Rôle de l'utilisateur") 