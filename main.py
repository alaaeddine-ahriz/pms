"""
PMS Protection Incendie - API Principal
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from config import settings
from database import create_tables

# Import des routes
from routes.auth import router as auth_router
from routes.common import router as common_router
from routes.referentiels import router as referentiels_router
from routes.documents import router as documents_router
from routes.hr import router as hr_router
from routes.vehicles import router as vehicles_router
from routes.materials import router as materials_router
from routes.products import router as products_router
from routes.projects import router as projects_router
from routes.manufacturing import router as manufacturing_router
from routes.finance import router as finance_router
from routes.logistics import router as logistics_router

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Métadonnées pour la documentation API
tags_metadata = [
    {
        "name": "Authentication",
        "description": "🔐 Authentification JWT et gestion des utilisateurs",
    },
    {
        "name": "Common",
        "description": "🏥 Points de contrôle généraux (santé, statut)",
    },
    {
        "name": "Reference Data",
        "description": "📋 Données de référence (devises, statuts, catégories)",
    },
    {
        "name": "Documents",
        "description": "📁 Gestion des documents (upload, métadonnées, tags)",
    },
    {
        "name": "Human Resources",
        "description": "👥 Gestion RH (employés, tâches, assignations)",
    },
    {
        "name": "Vehicles",
        "description": "🚗 Parc automobile (véhicules, kilométrages, conducteurs)",
    },
    {
        "name": "Materials",
        "description": "🔧 Gestion du matériel et équipements",
    },
    {
        "name": "Products & Stock",
        "description": "📦 Produits, articles, stocks et mouvements",
    },
    {
        "name": "Projects",
        "description": "🏗️ Gestion des projets et caisses",
    },
    {
        "name": "Manufacturing",
        "description": "🏭 Fabrication (nomenclatures, ordres, suivi)",
    },
    {
        "name": "Finance",
        "description": "💰 Comptabilité et grand livre",
    },
    {
        "name": "Logistics",
        "description": "🚚 Logistique (livraisons, approvisionnements)",
    },
]

# Création de l'application FastAPI avec documentation enrichie
app = FastAPI(
    title=settings.project_name,
    description=f"""
## 🚀 API PMS Protection Incendie

{settings.description}

### 🔐 Authentification
Cette API utilise l'authentification **JWT Bearer Token**.

1. **Connexion** : `POST /auth/login` avec email/password
2. **Utilisation** : Ajouter `Authorization: Bearer <token>` dans les headers
3. **Test rapide** : `admin@example.com` / `password123`

### 📖 Documentation
- **Swagger UI** : `/docs` (cette page)
- **ReDoc** : `/redoc` (documentation alternative)
- **Santé API** : `/health`

### 🎯 Fonctionnalités Principales
- ✅ Gestion complète des projets
- ✅ Suivi RH et équipes  
- ✅ Gestion de stock et fabrication
- ✅ Comptabilité double-entrée
- ✅ Logistique et approvisionnements

### 🔗 Liens Utiles
- [GitHub Repository](#)
- [Documentation Technique](README.md)
- [Guide de Démarrage Rapide](quick_start.py)
    """,
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=tags_metadata,
    contact={
        "name": "Support PMS Protection Incendie",
        "email": "support@pms-incendie.ma",
    },
    license_info={
        "name": "Propriétaire",
        "url": "https://www.pms-incendie.ma/license",
    },
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À configurer selon vos besoins en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware pour le timing des requêtes
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Gestionnaire d'erreurs global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.debug else "An error occurred"
        }
    )


# Événements de démarrage et d'arrêt
@app.on_event("startup")
async def startup_event():
    """Actions à effectuer au démarrage de l'application"""
    logger.info("Démarrage de l'API PMS Protection Incendie")
    logger.info(f"Version: {settings.version}")
    
    # Créer les tables de base de données
    try:
        create_tables()
        logger.info("Tables de base de données créées/vérifiées")
    except Exception as e:
        logger.error(f"Erreur lors de la création des tables: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Actions à effectuer à l'arrêt de l'application"""
    logger.info("Arrêt de l'API PMS Protection Incendie")


# Enregistrement des routes
app.include_router(common_router)
app.include_router(auth_router)
app.include_router(referentiels_router)
app.include_router(documents_router)
app.include_router(hr_router)
app.include_router(vehicles_router)
app.include_router(materials_router)
app.include_router(products_router)
app.include_router(projects_router)
app.include_router(manufacturing_router)
app.include_router(finance_router)
app.include_router(logistics_router)


# Route racine
@app.get("/")
async def root():
    """
    Page d'accueil de l'API
    """
    return {
        "name": settings.project_name,
        "version": settings.version,
        "description": settings.description,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


# Route de métriques (pour monitoring)
@app.get("/metrics")
async def metrics():
    """
    Endpoint pour les métriques Prometheus/OpenTelemetry
    """
    # TODO: Implémenter les métriques réelles
    return {
        "status": "ok",
        "metrics_available": False,
        "message": "Metrics endpoint not implemented yet"
    }


# Route admin pour créer des utilisateurs
@app.post("/admin/users")
async def create_platform_user():
    """
    Créer un utilisateur / binding de rôle pour la plateforme
    """
    # TODO: Implémenter la création d'utilisateurs admin
    raise HTTPException(status_code=501, detail="Not implemented yet")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 