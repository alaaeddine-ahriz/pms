#!/usr/bin/env python3
"""
Démonstration Swagger UI pour PMS Protection Incendie
Script pour tester et explorer l'API via l'interface Swagger
"""
import webbrowser
import time
import httpx
import asyncio
from datetime import datetime


def open_swagger_ui():
    """Ouvre automatiquement Swagger UI dans le navigateur"""
    print("🌐 Ouverture de Swagger UI...")
    
    # URLs principales
    swagger_url = "http://localhost:8000/docs"
    redoc_url = "http://localhost:8000/redoc"
    api_url = "http://localhost:8000"
    
    print(f"📖 Swagger UI : {swagger_url}")
    print(f"📚 ReDoc     : {redoc_url}")
    print(f"🔗 API Root  : {api_url}")
    
    # Ouvrir dans le navigateur par défaut
    try:
        webbrowser.open(swagger_url)
        print("✅ Swagger UI ouvert dans le navigateur !")
    except Exception as e:
        print(f"❌ Erreur d'ouverture navigateur: {e}")
        print(f"🔗 Veuillez ouvrir manuellement: {swagger_url}")


async def test_api_health():
    """Teste si l'API est accessible"""
    try:
        async with httpx.AsyncClient() as client:
            print("🔍 Test de connectivité API...")
            
            # Test de santé
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("✅ API accessible et fonctionnelle")
                health_data = response.json()
                print(f"   Status: {health_data.get('status', 'unknown')}")
                print(f"   Database: {health_data.get('database', 'unknown')}")
                return True
            else:
                print(f"⚠️ API répond avec code: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ API non accessible: {e}")
        print("🚀 Assurez-vous que l'API tourne avec: python3 main.py")
        return False


async def demo_login():
    """Démontre la connexion via l'API"""
    try:
        async with httpx.AsyncClient() as client:
            print("\n🔐 Démonstration de connexion...")
            
            login_data = {
                "email": "admin@example.com",
                "password": "password123"
            }
            
            response = await client.post(
                "http://localhost:8000/auth/login",
                json=login_data
            )
            
            if response.status_code == 200:
                token_data = response.json()
                token = token_data.get('access_token', '')
                print("✅ Connexion réussie !")
                print(f"🎫 Token: {token[:50]}...")
                print(f"⏰ Expire dans: {token_data.get('expires_in', 0)} secondes")
                
                # Test d'une route protégée
                headers = {"Authorization": f"Bearer {token}"}
                response = await client.get(
                    "http://localhost:8000/api/v1/devise",
                    headers=headers
                )
                
                if response.status_code == 200:
                    devises = response.json()
                    print(f"💰 {len(devises)} devises récupérées")
                    for devise in devises[:3]:  # Afficher les 3 premières
                        print(f"   - {devise.get('code', 'N/A')}: {devise.get('libelle', 'N/A')}")
                else:
                    print(f"⚠️ Erreur accès aux devises: {response.status_code}")
                    
            else:
                print(f"❌ Échec de connexion: {response.status_code}")
                print(f"   Réponse: {response.text}")
                
    except Exception as e:
        print(f"❌ Erreur lors de la connexion: {e}")


def print_swagger_guide():
    """Affiche un guide d'utilisation de Swagger UI"""
    print("\n" + "="*60)
    print("📖 GUIDE D'UTILISATION SWAGGER UI")
    print("="*60)
    
    print("""
🔹 SECTIONS PRINCIPALES :
   • Authentication : Connexion et tokens JWT
   • Reference Data : Données de base (devises, statuts...)
   • Human Resources : Employés et tâches
   • Vehicles : Gestion du parc automobile
   • Materials : Matériel et équipements
   • Products & Stock : Gestion des stocks
   • Projects : Projets et caisses
   • Manufacturing : Fabrication et ordres
   • Finance : Comptabilité
   • Logistics : Livraisons et approvisionnements

🔹 COMMENT TESTER :
   1. Cliquez sur "Authentication" > "/auth/login"
   2. Cliquez "Try it out"
   3. Utilisez : admin@example.com / password123
   4. Cliquez "Execute"
   5. Copiez le token de la réponse
   6. Cliquez "Authorize" (🔒 en haut à droite)
   7. Collez le token avec "Bearer " devant
   8. Maintenant vous pouvez tester toutes les routes !

🔹 FONCTIONNALITÉS UTILES :
   • Schémas : Voir la structure des données
   • Exemples : Données de test pré-remplies
   • Réponses : Codes de retour et formats
   • Autorisation : Gestion centralisée des tokens

🔹 ALTERNATIVES :
   • ReDoc : http://localhost:8000/redoc (plus lisible)
   • API Raw : http://localhost:8000/openapi.json
    """)


async def main():
    """Point d'entrée principal"""
    print("🚀 PMS Protection Incendie - Démonstration Swagger UI")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Test de connectivité
    api_ok = await test_api_health()
    
    if api_ok:
        # 2. Démonstration de connexion
        await demo_login()
        
        # 3. Ouverture de Swagger UI
        time.sleep(1)
        open_swagger_ui()
        
        # 4. Guide d'utilisation
        print_swagger_guide()
        
        print("\n🎉 Démonstration terminée !")
        print("📖 Swagger UI est maintenant ouvert dans votre navigateur")
        print("🔗 URL directe : http://localhost:8000/docs")
        
    else:
        print("\n❌ Impossible de démarrer la démonstration")
        print("🚀 Veuillez d'abord démarrer l'API avec: python3 main.py")


if __name__ == "__main__":
    asyncio.run(main()) 