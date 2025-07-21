#!/usr/bin/env python3
"""
Script de vérification de la configuration
Vérifie que tout est prêt avant le lancement de l'API
"""
import os
import sys
from pathlib import Path
import subprocess

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Changer vers le répertoire racine du projet
os.chdir(Path(__file__).parent.parent)

def check_python_version():
    """Vérifie la version de Python et l'environnement virtuel"""
    print("🐍 Vérification de Python...")
    version = sys.version_info
    
    # Vérifier l'environnement virtuel pyenv
    pyenv_version = os.environ.get('PYENV_VERSION')
    virtual_env = os.environ.get('VIRTUAL_ENV')
    
    if pyenv_version:
        print(f"  📦 Environnement pyenv: {pyenv_version}")
    if virtual_env:
        print(f"  🏠 Environnement virtuel: {virtual_env}")
    
    # Vérifier si on est dans venv-3.12
    if not (pyenv_version == 'venv-3.12' or 'venv-3.12' in str(virtual_env)):
        print("  ⚠️  Vous devriez utiliser l'environnement venv-3.12")
        print("  🔧 Activez avec: pyenv activate venv-3.12")
        print("  📝 Ou créez-le: pyenv virtualenv 3.12 venv-3.12")
    
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✅ Python {version.major}.{version.minor} OK")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor} trop ancien (minimum: 3.8)")
        return False

def check_dependencies():
    """Vérifie les dépendances"""
    print("📦 Vérification des dépendances...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'sqlalchemy', 'psycopg2', 
        'pydantic', 'pydantic_settings', 'jose'  # python_jose s'importe comme 'jose'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} manquant")
            missing.append(package)
    
    if missing:
        print("\n🔧 Installez les dépendances manquantes:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_environment_files():
    """Vérifie les fichiers d'environnement"""
    print("🔧 Vérification des environnements...")
    
    environments = {
        'config/.env.dev': 'Développement',
        'config/.env.prod': 'Production', 
        'config/.env.test': 'Test'
    }
    
    configured = 0
    for env_file, env_name in environments.items():
        if Path(env_file).exists():
            print(f"  ✅ {env_name}: {env_file}")
            configured += 1
        else:
            print(f"  ⚠️  {env_name}: {env_file} manquant")
    
    if configured == 0:
        print("\n🚀 Configurez au moins un environnement:")
        print("   python3 scripts/setup_env.py dev")
        return False
    
    return True

def check_database_config():
    """Vérifie la configuration de base de données"""
    print("🗄️  Vérification de la configuration DB...")
    
    try:
        # Test de chargement de la config
        os.environ.setdefault("ENVIRONMENT", "development")
        from config import settings
        
        if settings.database_url:
            print(f"  ✅ URL de DB configurée")
            print(f"  📊 Environnement: {os.environ.get('ENVIRONMENT', 'non défini')}")
            return True
        else:
            print("  ❌ URL de DB manquante")
            return False
            
    except Exception as e:
        print(f"  ❌ Erreur de configuration: {e}")
        return False

def check_directories():
    """Vérifie les dossiers nécessaires"""
    print("📁 Vérification des dossiers...")
    
    directories = ['uploads', 'uploads/dev']
    
    for directory in directories:
        dir_path = Path(directory)
        if dir_path.exists():
            print(f"  ✅ {directory}/")
        else:
            print(f"  ⚠️  {directory}/ créé")
            dir_path.mkdir(parents=True, exist_ok=True)
    
    return True

def check_ports():
    """Vérifie la disponibilité des ports"""
    print("🌐 Vérification des ports...")
    
    import socket
    
    ports_to_check = [
        (8000, "Développement"),
        (80, "Production (nécessite sudo)"),
    ]
    
    available_ports = 0
    for port, description in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('127.0.0.1', port))
            print(f"  ✅ Port {port} libre ({description})")
            available_ports += 1
        except OSError:
            print(f"  ⚠️  Port {port} occupé ({description})")
        finally:
            sock.close()
    
    return available_ports > 0

def test_import():
    """Test d'import de l'application"""
    print("🧪 Test d'import de l'application...")
    
    try:
        # Test d'import sans démarrer l'app
        import main
        print("  ✅ Import principal OK")
        
        from config import settings, get_environment_info
        env_info = get_environment_info()
        print(f"  ✅ Configuration chargée: {env_info['config_class']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur d'import: {e}")
        return False

def main():
    """Point d'entrée principal"""
    print("🔍 Vérification de la configuration PMS Protection Incendie")
    print("=" * 60)
    
    checks = [
        ("Version Python", check_python_version),
        ("Dépendances", check_dependencies),
        ("Fichiers d'environnement", check_environment_files),
        ("Configuration DB", check_database_config),
        ("Dossiers", check_directories),
        ("Ports réseau", check_ports),
        ("Import application", test_import),
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print()
        if check_func():
            passed += 1
        else:
            print(f"⚠️  {name}: Problème détecté")
    
    print("\n" + "=" * 60)
    print(f"📊 Résultat: {passed}/{total} vérifications réussies")
    
    if passed == total:
        print("🎉 Tout est configuré correctement !")
        print("🚀 Prêt à lancer l'API:")
        print("   python3 start_dev.py")
        return True
    else:
        print("⚠️  Des problèmes ont été détectés")
        print("🔧 Consultez les messages ci-dessus pour résoudre les problèmes")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 