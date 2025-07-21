#!/usr/bin/env python3
"""
Script pour créer le premier utilisateur administrateur
"""
import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))
os.chdir(Path(__file__).parent.parent)

from sqlalchemy.orm import Session
from database import SessionLocal, create_tables
from models.hr import Employe
from models.referentiels import FonctionEmploye
from auth import get_password_hash


def create_admin_user():
    """Crée un utilisateur administrateur"""
    
    print("🔧 Création du premier utilisateur administrateur")
    print("=" * 50)
    
    # Créer les tables si elles n'existent pas
    try:
        create_tables()
        print("✅ Tables de base de données vérifiées")
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        return False
    
    # Créer une session de base de données
    db: Session = SessionLocal()
    
    try:
        # Vérifier si un admin existe déjà
        existing_admin = db.query(Employe).filter(
            Employe.role == "admin"
        ).first()
        
        if existing_admin:
            print(f"✅ Un administrateur existe déjà: {existing_admin.email}")
            print(f"   Nom: {existing_admin.prenom} {existing_admin.nom}")
            return True
        
        # Créer la fonction "Administrateur" si elle n'existe pas
        admin_fonction = db.query(FonctionEmploye).filter(
            FonctionEmploye.libelle == "Administrateur"
        ).first()
        
        if not admin_fonction:
            admin_fonction = FonctionEmploye(
                libelle="Administrateur",
                description="Accès complet au système"
            )
            db.add(admin_fonction)
            db.commit()
            db.refresh(admin_fonction)
            print("✅ Fonction 'Administrateur' créée")
        
        # Données de l'administrateur par défaut
        admin_data = {
            "nom": "Admin",
            "prenom": "Super", 
            "email": "admin@mail.com",
            "password": "admin123",  # À changer lors de la première connexion
            "role": "admin"
        }
        
        print(f"\n👤 Création de l'utilisateur administrateur:")
        print(f"   Email: {admin_data['email']}")
        print(f"   Mot de passe temporaire: {admin_data['password']}")
        print(f"   ⚠️  CHANGEZ CE MOT DE PASSE dès la première connexion!")
        
        # Créer l'utilisateur admin
        admin_user = Employe(
            nom=admin_data["nom"],
            prenom=admin_data["prenom"],
            email=admin_data["email"],
            password_hash=get_password_hash(admin_data["password"]),
            role=admin_data["role"],
            id_fonction=admin_fonction.id_fonction,
            is_active="1"
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"\n🎉 Utilisateur administrateur créé avec succès!")
        print(f"   ID: {admin_user.id_employe}")
        print(f"   Email: {admin_user.email}")
        print(f"   Rôle: {admin_user.role}")
        
        print(f"\n🔐 Test de connexion:")
        print(f"curl -X POST http://127.0.0.1:8000/auth/login \\")
        print(f'  -H "Content-Type: application/json" \\')
        print(f'  -d \'{{"email":"{admin_data["email"]}","password":"{admin_data["password"]}"}}\'')
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'utilisateur: {e}")
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    success = create_admin_user()
    if success:
        print(f"\n✅ Prêt! Vous pouvez maintenant vous connecter à l'API")
        print(f"📖 Documentation: http://127.0.0.1:8000/docs")
    else:
        print(f"\n❌ Échec de la création de l'utilisateur")
        sys.exit(1) 