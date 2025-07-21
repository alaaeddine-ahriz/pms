#!/usr/bin/env python3
"""
Script de gestion de la base de données PMS Incendie
"""
import os
import sys
import subprocess
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))
os.chdir(Path(__file__).parent.parent)

def run_command(cmd, check=True):
    """Exécuter une commande shell"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return None

def is_container_running():
    """Vérifier si le container PostgreSQL est en marche"""
    result = run_command("docker ps --filter name=pms-postgres-dev --format '{{.Names}}'", check=False)
    return "pms-postgres-dev" in result if result else False

def start_db():
    """Démarrer la base de données"""
    print("🚀 Démarrage de PostgreSQL...")
    run_command("docker-compose -f config/docker-compose.dev.yml up -d")
    print("✅ PostgreSQL démarré")

def stop_db():
    """Arrêter la base de données"""
    print("🛑 Arrêt de PostgreSQL...")
    run_command("docker-compose -f config/docker-compose.dev.yml down")
    print("✅ PostgreSQL arrêté")

def reset_db():
    """Réinitialiser complètement la base de données"""
    print("⚠️  ATTENTION: Cette action va SUPPRIMER toutes les données!")
    response = input("Êtes-vous sûr? (tapez 'RESET' pour confirmer): ")
    if response != "RESET":
        print("❌ Opération annulée")
        return
    
    print("🗑️  Suppression des données...")
    run_command("docker-compose -f config/docker-compose.dev.yml down -v")
    print("🚀 Recréation de la base...")
    run_command("docker-compose -f config/docker-compose.dev.yml up -d")
    print("✅ Base de données réinitialisée")

def status_db():
    """Afficher le statut de la base de données"""
    if is_container_running():
        print("✅ PostgreSQL est en marche")
        
        # Statistiques des tables
        stats_cmd = """
        docker exec pms-postgres-dev psql -U dev_user -d pms_incendie_dev -c "
        SELECT 
            schemaname, relname as table_name, 
            n_tup_ins as inserts,
            n_tup_upd as updates,
            n_tup_del as deletes,
            n_live_tup as rows
        FROM pg_stat_user_tables 
        WHERE n_live_tup > 0
        ORDER BY n_live_tup DESC;
        "
        """
        print("\n📊 Statistiques des tables:")
        run_command(stats_cmd)
    else:
        print("❌ PostgreSQL n'est pas en marche")

def psql_connect():
    """Se connecter à psql"""
    if not is_container_running():
        print("❌ PostgreSQL n'est pas en marche. Démarrez-le d'abord avec: python3 scripts/manage_db.py start")
        return
    
    print("🔗 Connexion à PostgreSQL...")
    print("💡 Commandes utiles:")
    print("   \\dt              - Lister les tables")
    print("   \\d employe       - Structure table employe") 
    print("   \\q               - Quitter")
    print("─" * 50)
    os.system("docker exec -it pms-postgres-dev psql -U dev_user -d pms_incendie_dev")

def backup_db():
    """Créer une sauvegarde de la base"""
    if not is_container_running():
        print("❌ PostgreSQL n'est pas en marche")
        return
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"database/backup_{timestamp}.sql"
    
    print(f"💾 Création d'une sauvegarde: {backup_file}")
    cmd = f"docker exec pms-postgres-dev pg_dump -U dev_user -d pms_incendie_dev > {backup_file}"
    run_command(cmd)
    print(f"✅ Sauvegarde créée: {backup_file}")

def show_help():
    """Afficher l'aide"""
    print("""
🗄️  Gestionnaire de Base de Données PMS Incendie

Usage: python3 scripts/manage_db.py <command>

Commandes disponibles:
  start     - Démarrer PostgreSQL
  stop      - Arrêter PostgreSQL  
  status    - Afficher le statut et les statistiques
  reset     - Réinitialiser la base (SUPPRIME TOUT!)
  psql      - Se connecter à psql
  backup    - Créer une sauvegarde
  help      - Afficher cette aide

Exemples:
  python3 scripts/manage_db.py start
  python3 scripts/manage_db.py psql
  python3 scripts/manage_db.py backup
    """)

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        'start': start_db,
        'stop': stop_db,
        'status': status_db,
        'reset': reset_db,
        'psql': psql_connect,
        'backup': backup_db,
        'help': show_help
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"❌ Commande inconnue: {command}")
        show_help()

if __name__ == "__main__":
    main() 