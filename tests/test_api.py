#!/usr/bin/env python3
"""
Script de test pour l'API PMS Protection Incendie
"""
import httpx
import asyncio
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"


async def test_api():
    """Test basique de l'API"""
    
    async with httpx.AsyncClient() as client:
        print("🔄 Test de l'API PMS Protection Incendie")
        print("=" * 50)
        
        # Test de santé
        print("\n1. Test de santé de l'API")
        response = await client.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test de la page d'accueil
        print("\n2. Test de la page d'accueil")
        response = await client.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test de connexion
        print("\n3. Test de connexion")
        login_data = {
            "email": "admin@example.com",
            "password": "password123"
        }
        response = await client.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"Token obtenu: {token_data['access_token'][:50]}...")
            token = token_data['access_token']
            
            # Test d'accès à une route protégée
            print("\n4. Test d'accès aux devises (route protégée)")
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{BASE_URL}/api/v1/devise", headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            # Test de création d'une devise
            print("\n5. Test de création d'une devise")
            devise_data = {
                "code": "EUR",
                "libelle": "Euro"
            }
            response = await client.post(
                f"{BASE_URL}/api/v1/devise", 
                json=devise_data, 
                headers=headers
            )
            print(f"Status: {response.status_code}")
            if response.status_code in [200, 201]:
                print(f"Response: {response.json()}")
            else:
                print(f"Error: {response.text}")
        else:
            print(f"Erreur de connexion: {response.text}")
        
        print("\n✅ Tests terminés")


def create_sample_data_sql():
    """Crée un fichier SQL avec des données d'exemple"""
    sql_content = """
-- Données d'exemple pour PMS Protection Incendie

-- Devises
INSERT INTO devise (code, libelle) VALUES 
('MAD', 'Dirham Marocain'),
('EUR', 'Euro'),
('USD', 'Dollar Américain')
ON CONFLICT (code) DO NOTHING;

-- Catégories de dépenses
INSERT INTO expense_category (libelle) VALUES 
('CARBURANT'),
('MAINTENANCE'),
('FOURNITURES'),
('TRANSPORT'),
('REPAS')
ON CONFLICT (libelle) DO NOTHING;

-- Statuts de fabrication
INSERT INTO statut_fabrication (libelle) VALUES 
('EN_ATTENTE'),
('EN_COURS'),
('TERMINE'),
('SUSPENDU')
ON CONFLICT (libelle) DO NOTHING;

-- Statuts de livraison
INSERT INTO statut_livraison (libelle) VALUES 
('PLANIFIEE'),
('EN_TRANSIT'),
('LIVREE'),
('RETARDEE')
ON CONFLICT (libelle) DO NOTHING;

-- Statuts d'approvisionnement
INSERT INTO statut_appro (libelle) VALUES 
('DEMANDEE'),
('VALIDEE'),
('COMMANDEE'),
('RECUE')
ON CONFLICT (libelle) DO NOTHING;

-- Tags de documents
INSERT INTO tag_document (libelle, description) VALUES 
('CONTRAT', 'Documents contractuels'),
('FACTURE', 'Factures et documents comptables'),
('TECHNIQUE', 'Documents techniques'),
('PHOTO', 'Photos de chantier'),
('CERTIF', 'Certificats et agréments')
ON CONFLICT (libelle) DO NOTHING;

-- Fonctions employés
INSERT INTO fonction_employe (libelle, description) VALUES 
('CHEF_CHANTIER', 'Chef de chantier'),
('TECHNICIEN', 'Technicien installation'),
('CONDUCTEUR', 'Conducteur véhicule'),
('ADMINISTRATIF', 'Personnel administratif'),
('COMMERCIAL', 'Commercial')
ON CONFLICT (libelle) DO NOTHING;

-- Entreprises (clients/fournisseurs)
INSERT INTO entreprise (raison_sociale, adresse, ice) VALUES 
('ONCF', 'Rabat, Maroc', '123456789'),
('OCP Group', 'Casablanca, Maroc', '987654321'),
('Suplec Maroc', 'Rabat, Maroc', '456789123')
ON CONFLICT (raison_sociale) DO NOTHING;
"""
    
    with open("sample_data.sql", "w", encoding="utf-8") as f:
        f.write(sql_content)
    
    print("📄 Fichier sample_data.sql créé avec des données d'exemple")


if __name__ == "__main__":
    print("🚀 Script de test API PMS Protection Incendie")
    print("\n1. Création des données d'exemple")
    create_sample_data_sql()
    
    print("\n2. Test de l'API (assurez-vous que l'API tourne sur localhost:8000)")
    try:
        asyncio.run(test_api())
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        print("Assurez-vous que l'API est démarrée avec: python main.py") 