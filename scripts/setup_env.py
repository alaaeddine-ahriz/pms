#!/usr/bin/env python3
"""
Script utilitaire pour configurer les environnements
Usage: python3 scripts/setup_env.py [dev|prod|test]
"""
import os
import sys
import shutil
import secrets
from pathlib import Path

# Changer vers le répertoire racine du projet
os.chdir(Path(__file__).parent.parent)

def generate_secret_key(length=64):
    """Génère une clé secrète sécurisée"""
    return secrets.token_urlsafe(length)

def setup_development():
    """Configure l'environnement de développement"""
    print("🔧 Configuration de l'environnement de DÉVELOPPEMENT")
    
    # Copier le fichier example
    source = Path("config/env.dev.example")
    target = Path("config/.env.dev")
    
    if target.exists():
        print(f"⚠️  Le fichier {target} existe déjà")
        response = input("Voulez-vous le remplacer? (y/N): ")
        if response.lower() != 'y':
            print("❌ Configuration annulée")
            return False
    
    if not source.exists():
        print(f"❌ Fichier source {source} introuvable")
        return False
    
    shutil.copy(source, target)
    
    # Créer les dossiers nécessaires
    uploads_dir = Path("uploads/dev")
    uploads_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"✅ Fichier {target} créé")
    print(f"✅ Dossier {uploads_dir} créé")
    print(f"🚀 Prêt pour le développement!")
    print(f"   Lancez: python3 scripts/start_dev.py")
    return True

def setup_production():
    """Configure l'environnement de production"""
    print("🏭 Configuration de l'environnement de PRODUCTION")
    print("⚠️  ATTENTION: Configuration sécurisée requise!")
    
    # Copier le fichier example
    source = Path("config/env.prod.example")
    target = Path("config/.env.prod")
    
    if target.exists():
        print(f"⚠️  Le fichier {target} existe déjà")
        response = input("Voulez-vous le remplacer? (y/N): ")
        if response.lower() != 'y':
            print("❌ Configuration annulée")
            return False
    
    if not source.exists():
        print(f"❌ Fichier source {source} introuvable")
        return False
    
    shutil.copy(source, target)
    
    # Générer une clé secrète sécurisée
    secret_key = generate_secret_key()
    
    # Remplacer les valeurs par défaut
    with open(target, 'r') as f:
        content = f.read()
    
    # Remplacer la clé secrète
    content = content.replace(
        "SECRET_KEY=MUST-BE-CHANGED-TO-SECURE-RANDOM-STRING-IN-PRODUCTION",
        f"SECRET_KEY={secret_key}"
    )
    
    with open(target, 'w') as f:
        f.write(content)
    
    # Créer les dossiers nécessaires
    uploads_dir = Path("uploads/prod")
    uploads_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"✅ Fichier {target} créé")
    print(f"🔑 Clé secrète générée automatiquement")
    print(f"✅ Dossier {uploads_dir} créé")
    print("")
    print("🔴 IMPORTANT: Vous devez encore configurer:")
    print("   1. Les identifiants de base de données PostgreSQL")
    print("   2. Les domaines CORS autorisés")
    print("   3. Le dossier d'upload (/var/pms/uploads)")
    print("")
    print(f"📝 Éditez le fichier {target} avant le lancement")
    print(f"🚀 Puis lancez: python3 scripts/start_prod.py")
    return True

def setup_test():
    """Configure l'environnement de test"""
    print("🧪 Configuration de l'environnement de TEST")
    
    # Créer un fichier de test basique
    target = Path("config/.env.test")
    
    if target.exists():
        print(f"⚠️  Le fichier {target} existe déjà")
        response = input("Voulez-vous le remplacer? (y/N): ")
        if response.lower() != 'y':
            print("❌ Configuration annulée")
            return False
    
    test_config = """# Configuration de TEST
ENVIRONMENT=test
DATABASE_URL=postgresql://test_user:test_password@localhost:5434/pms_incendie_test
SECRET_KEY=test-secret-key-for-testing-only
ACCESS_TOKEN_EXPIRE_MINUTES=5
DEBUG=true
LOG_LEVEL=WARNING
UPLOAD_DIR=uploads/test
"""
    
    with open(target, 'w') as f:
        f.write(test_config)
    
    # Créer les dossiers nécessaires
    uploads_dir = Path("uploads/test")
    uploads_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"✅ Fichier {target} créé")
    print(f"✅ Dossier {uploads_dir} créé")
    print(f"🧪 Prêt pour les tests!")
    return True

def show_status():
    """Affiche le statut des environnements"""
    print("📊 Statut des environnements:")
    print("=" * 40)
    
    environments = [
        ("config/.env.dev", "Développement", "scripts/start_dev.py"),
        ("config/.env.prod", "Production", "scripts/start_prod.py"),
        ("config/.env.test", "Test", "pytest"),
    ]
    
    for env_file, env_name, launch_cmd in environments:
        if Path(env_file).exists():
            print(f"✅ {env_name:12} : {env_file} (lancez: {launch_cmd})")
        else:
            print(f"❌ {env_name:12} : {env_file} manquant")
    
    print("")
    print("🚀 Pour configurer un environnement:")
    print("   python3 scripts/setup_env.py dev   # Développement")
    print("   python3 scripts/setup_env.py prod  # Production")
    print("   python3 scripts/setup_env.py test  # Test")

def main():
    """Point d'entrée principal"""
    if len(sys.argv) != 2:
        show_status()
        return
    
    env_type = sys.argv[1].lower()
    
    if env_type in ['dev', 'development']:
        setup_development()
    elif env_type in ['prod', 'production']:
        setup_production()
    elif env_type in ['test', 'testing']:
        setup_test()
    else:
        print(f"❌ Environnement '{env_type}' non reconnu")
        print("✅ Environnements disponibles: dev, prod, test")
        sys.exit(1)

if __name__ == "__main__":
    main() 