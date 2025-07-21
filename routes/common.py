"""
Routes communes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from schemas.common import ResponseMessage

router = APIRouter(tags=["Common"])


@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Vérification de l'état de l'API et de la base de données
    """
    try:
        # Test de connexion à la base de données
        result = db.execute(text("SELECT 1"))
        result.fetchone()
        
        return {
            "status": "healthy",
            "database": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        } 