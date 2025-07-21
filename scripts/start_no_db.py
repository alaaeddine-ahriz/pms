#!/usr/bin/env python3
"""
Script de lancement SANS base de données
Pour les tests d'API sans configuration PostgreSQL
Usage: python3 scripts/start_no_db.py
"""
import os
import sys
import uvicorn
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    """Lance l'API sans base de données"""
    
    # Forcer l'environnement de développement
    os.environ["ENVIRONMENT"] = "development"
    
    # Configurer pour SQLite (plus simple)
    os.environ["DATABASE_URL"] = "sqlite:///./test.db"
    
    print("🚀 Démarrage de l'API PMS Protection Incendie")
    print("⚠️  Mode SANS PostgreSQL (base SQLite temporaire)")
    print("🔧 Environnement: DÉVELOPPEMENT")
    print("🌐 URL: http://127.0.0.1:8000")
    print("📖 Documentation: http://127.0.0.1:8000/docs")
    print("=" * 50)
    print("ℹ️  Pour une configuration complète, installez PostgreSQL")
    print("   ou utilisez Docker: docker-compose -f config/docker-compose.dev.yml up -d")
    print("=" * 50)
    
    # Configuration pour le développement avec SQLite
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["./"],
        reload_excludes=["uploads/*", "*.log", "__pycache__", "*.db"],
        log_level="debug",
        access_log=True,
        use_colors=True
    )

if __name__ == "__main__":
    main() 