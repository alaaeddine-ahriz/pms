"""
Gestion de l'authentification JWT
"""
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from config import settings
from database import get_db

# Contexte de chiffrement pour les mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Schéma de sécurité Bearer Token
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe contre son hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Génère le hash d'un mot de passe"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crée un token JWT d'accès
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Vérifie et décode un token JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return {
            "user_id": int(user_id),
            "email": payload.get("email"),
            "role": payload.get("role")
        }
    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    """
    Dépendance pour récupérer l'utilisateur courant à partir du token
    """
    from models.hr import Employe  # Import ici pour éviter les imports circulaires
    
    token_data = verify_token(token.credentials)
    user_id = token_data["user_id"]
    
    # Récupérer l'utilisateur depuis la base de données
    user = db.query(Employe).filter(
        Employe.id_employe == user_id,
        Employe.is_active == "1"
    ).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def require_role(required_role: str):
    """
    Décorateur pour exiger un rôle spécifique
    """
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role != required_role and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: {required_role}"
            )
        return current_user
    return role_checker 