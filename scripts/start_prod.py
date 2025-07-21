#!/usr/bin/env python3
"""
Script de lancement pour l'environnement de PRODUCTION
Usage: python3 start_prod.py
"""
import os
import sys
import uvicorn
from pathlib import Path

def main():
    """Lance l'API en mode production"""
    
    # Forcer l'environnement de production
    os.environ["ENVIRONMENT"] = "production"
    
    # Vérifier que le fichier de config prod existe
    env_file = Path(".env.prod")
    if not env_file.exists():
        print("❌ Fichier .env.prod introuvable!")
        print("📝 Copiez env.prod.example vers .env.prod:")
        print("   cp env.prod.example .env.prod")
        print("⚠️  N'oubliez pas de changer les mots de passe et clés secrètes!")
        sys.exit(1)
    
    # Vérifier les variables critiques de sécurité
    with open(".env.prod", "r") as f:
        content = f.read()
        if "MUST-BE-CHANGED" in content or "CHANGE_THIS" in content:
            print("❌ ERREUR DE SÉCURITÉ!")
            print("⚠️  Vous devez changer les mots de passe dans .env.prod")
            print("📝 Recherchez les chaînes 'MUST-BE-CHANGED' et 'CHANGE_THIS'")
            sys.exit(1)
    
    # Créer le dossier uploads production s'il n'existe pas
    uploads_dir = Path("/var/pms/uploads")
    try:
        uploads_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        # Fallback vers un dossier local
        uploads_dir = Path("uploads/prod")
        uploads_dir.mkdir(parents=True, exist_ok=True)
        print(f"⚠️  Utilisation du dossier local: {uploads_dir}")
    
    print("🚀 Démarrage de l'API PMS Protection Incendie")
    print("🏭 Environnement: PRODUCTION")
    print("📁 Config: .env.prod")
    print("🌐 URL: http://0.0.0.0:80")
    print("🔒 Mode sécurisé: Documentation désactivée")
    print("═" * 50)
    
    # Configuration pour la production
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80,
        reload=False,
        log_level="warning",
        access_log=False,
        use_colors=False,
        workers=4  # Plusieurs workers pour la production
    )

if __name__ == "__main__":
    main() 