#!/usr/bin/env python3
"""
Script de lancement pour l'environnement de DÉVELOPPEMENT
Usage: python3 scripts/start_dev.py
"""
import os
import sys
import uvicorn
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    """Lance l'API en mode développement"""
    
    # Forcer l'environnement de développement
    os.environ["ENVIRONMENT"] = "development"
    
    # Vérifier que le fichier de config dev existe
    env_file = Path("config/.env.dev")
    if not env_file.exists():
        print("❌ Fichier config/.env.dev introuvable!")
        print("📝 Copiez config/env.dev.example vers config/.env.dev:")
        print("   cp config/env.dev.example config/.env.dev")
        sys.exit(1)
    
    # Créer le dossier uploads s'il n'existe pas
    uploads_dir = Path("uploads/dev")
    uploads_dir.mkdir(parents=True, exist_ok=True)
    
    print("🚀 Démarrage de l'API PMS Protection Incendie")
    print("🔧 Environnement: DÉVELOPPEMENT")
    print("📁 Config: config/.env.dev")
    print("🌐 URL: http://127.0.0.1:8000")
    print("📖 Documentation: http://127.0.0.1:8000/docs")
    print("═" * 50)
    
    # Configuration pour le développement
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["./"],
        reload_excludes=["uploads/*", "*.log", "__pycache__"],
        log_level="debug",
        access_log=True,
        use_colors=True
    )

if __name__ == "__main__":
    main() 