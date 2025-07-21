#!/usr/bin/env python3
"""
Script de démarrage rapide pour PMS Protection Incendie
Initialise la base de données avec des données d'exemple
"""
import asyncio
from datetime import date
from sqlalchemy.orm import Session
from database import create_tables, SessionLocal
from models import *


def create_sample_data():
    """Crée des données d'exemple pour tester l'API"""
    db = SessionLocal()
    
    try:
        print("🚀 Création des données d'exemple...")
        
        # Créer des devises
        devises = [
            Devise(code="MAD", libelle="Dirham Marocain"),
            Devise(code="EUR", libelle="Euro"),
            Devise(code="USD", libelle="Dollar Américain")
        ]
        
        for devise in devises:
            existing = db.query(Devise).filter(Devise.code == devise.code).first()
            if not existing:
                db.add(devise)
                print(f"💰 Devise ajoutée: {devise.code}")
        
        # Créer des catégories de dépenses
        categories = [
            ExpenseCategory(libelle="CARBURANT"),
            ExpenseCategory(libelle="MAINTENANCE"),
            ExpenseCategory(libelle="FOURNITURES"),
            ExpenseCategory(libelle="TRANSPORT"),
            ExpenseCategory(libelle="REPAS")
        ]
        
        for category in categories:
            existing = db.query(ExpenseCategory).filter(ExpenseCategory.libelle == category.libelle).first()
            if not existing:
                db.add(category)
                print(f"📋 Catégorie ajoutée: {category.libelle}")
        
        # Créer des statuts
        statuts_fab = [
            StatutFabrication(libelle="EN_ATTENTE"),
            StatutFabrication(libelle="EN_COURS"),
            StatutFabrication(libelle="TERMINE"),
            StatutFabrication(libelle="SUSPENDU")
        ]
        
        for statut in statuts_fab:
            existing = db.query(StatutFabrication).filter(StatutFabrication.libelle == statut.libelle).first()
            if not existing:
                db.add(statut)
                print(f"🏭 Statut fabrication ajouté: {statut.libelle}")
        
        statuts_liv = [
            StatutLivraison(libelle="PLANIFIEE"),
            StatutLivraison(libelle="EN_TRANSIT"),
            StatutLivraison(libelle="LIVREE"),
            StatutLivraison(libelle="RETARDEE")
        ]
        
        for statut in statuts_liv:
            existing = db.query(StatutLivraison).filter(StatutLivraison.libelle == statut.libelle).first()
            if not existing:
                db.add(statut)
                print(f"🚚 Statut livraison ajouté: {statut.libelle}")
        
        statuts_appro = [
            StatutAppro(libelle="DEMANDEE"),
            StatutAppro(libelle="VALIDEE"),
            StatutAppro(libelle="COMMANDEE"),
            StatutAppro(libelle="RECUE")
        ]
        
        for statut in statuts_appro:
            existing = db.query(StatutAppro).filter(StatutAppro.libelle == statut.libelle).first()
            if not existing:
                db.add(statut)
                print(f"📦 Statut appro ajouté: {statut.libelle}")
        
        # Créer des fonctions d'employés
        fonctions = [
            FonctionEmploye(libelle="CHEF_CHANTIER", description="Chef de chantier"),
            FonctionEmploye(libelle="TECHNICIEN", description="Technicien installation"),
            FonctionEmploye(libelle="CONDUCTEUR", description="Conducteur véhicule"),
            FonctionEmploye(libelle="ADMINISTRATIF", description="Personnel administratif"),
            FonctionEmploye(libelle="COMMERCIAL", description="Commercial")
        ]
        
        for fonction in fonctions:
            existing = db.query(FonctionEmploye).filter(FonctionEmploye.libelle == fonction.libelle).first()
            if not existing:
                db.add(fonction)
                print(f"👤 Fonction ajoutée: {fonction.libelle}")
        
        # Créer des entreprises
        entreprises = [
            Entreprise(raison_sociale="ONCF", adresse="Rabat, Maroc", ice="123456789"),
            Entreprise(raison_sociale="OCP Group", adresse="Casablanca, Maroc", ice="987654321"),
            Entreprise(raison_sociale="Suplec Maroc", adresse="Rabat, Maroc", ice="456789123")
        ]
        
        for entreprise in entreprises:
            existing = db.query(Entreprise).filter(Entreprise.raison_sociale == entreprise.raison_sociale).first()
            if not existing:
                db.add(entreprise)
                print(f"🏢 Entreprise ajoutée: {entreprise.raison_sociale}")
        
        # Créer des tags de documents
        tags = [
            TagDocument(libelle="CONTRAT", description="Documents contractuels"),
            TagDocument(libelle="FACTURE", description="Factures et documents comptables"),
            TagDocument(libelle="TECHNIQUE", description="Documents techniques"),
            TagDocument(libelle="PHOTO", description="Photos de chantier"),
            TagDocument(libelle="CERTIF", description="Certificats et agréments")
        ]
        
        for tag in tags:
            existing = db.query(TagDocument).filter(TagDocument.libelle == tag.libelle).first()
            if not existing:
                db.add(tag)
                print(f"🏷️ Tag ajouté: {tag.libelle}")
        
        # Créer un stock par défaut
        stock_principal = Stock(libelle="Stock Principal", adresse="Entrepôt principal - Casablanca")
        existing_stock = db.query(Stock).filter(Stock.libelle == stock_principal.libelle).first()
        if not existing_stock:
            db.add(stock_principal)
            print(f"📦 Stock ajouté: {stock_principal.libelle}")
        
        # Créer quelques produits d'exemple
        produits = [
            Produit(code_produit="EXT001", libelle="Extincteur 6L", description="Extincteur à poudre 6L"),
            Produit(code_produit="DET001", libelle="Détecteur fumée", description="Détecteur de fumée optique"),
            Produit(code_produit="TUY001", libelle="Tuyau incendie 20m", description="Tuyau d'incendie 20 mètres")
        ]
        
        for produit in produits:
            existing = db.query(Produit).filter(Produit.code_produit == produit.code_produit).first()
            if not existing:
                db.add(produit)
                print(f"🔧 Produit ajouté: {produit.code_produit}")
        
        # Commiter toutes les données
        db.commit()
        print("✅ Données d'exemple créées avec succès!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de la création des données: {e}")
        
    finally:
        db.close()


def main():
    """Point d'entrée principal"""
    print("🚀 PMS Protection Incendie - Démarrage rapide")
    print("=" * 50)
    
    print("\n1. Création des tables...")
    try:
        create_tables()
        print("✅ Tables créées avec succès!")
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        return
    
    print("\n2. Création des données d'exemple...")
    create_sample_data()
    
    print("\n🎉 Démarrage rapide terminé!")
    print("\n📋 Prochaines étapes:")
    print("1. Démarrer l'API: python3 main.py")
    print("2. Ouvrir la documentation: http://localhost:8000/docs")
    print("3. Tester la connexion: admin@example.com / password123")


if __name__ == "__main__":
    main() 