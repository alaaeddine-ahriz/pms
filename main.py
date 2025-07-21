"""
PMS Protection Incendie - API Principal
Support des environnements multiples (dev, prod, test)
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from config import settings, get_environment_info, get_cors_origins_list
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

# Configuration du logging selon l'environnement
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
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

# Création de l'application FastAPI avec configuration dynamique
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
    docs_url="/docs" if getattr(settings, 'enable_docs', True) else None,
    redoc_url="/redoc" if getattr(settings, 'enable_redoc', True) else None,
    openapi_tags=tags_metadata,
    contact={
        "name": "Support PMS Protection Incendie",
        "email": "alaaahriz@gmail.com",
    },
    license_info={
        "name": "Propriétaire",
    },
)

# Middleware CORS configuré selon l'environnement
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins_list(),
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
    env_info = get_environment_info()
    
    logger.info("Démarrage de l'API PMS Protection Incendie")
    logger.info(f"Version: {settings.version}")
    logger.info(f"Environnement: {env_info['environment']}")
    logger.info(f"Configuration: {env_info['config_class']}")
    logger.info(f"Debug: {env_info['debug_mode']}")
    logger.info(f"Port: {env_info['port']}")
    
    # Créer les tables de base de données
    try:
        create_tables()
        logger.info("Tables de base de données créées/vérifiées")
    except Exception as e:
        logger.warning(f"Base de données non disponible: {e}")
        logger.warning("L'API démarre en mode sans base de données")
        logger.warning("Certaines fonctionnalités nécessiteront une DB")

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
    env_info = get_environment_info()
    return {
        "name": settings.project_name,
        "version": settings.version,
        "description": settings.description,
        "environment": env_info["environment"],
        "docs": "/docs" if env_info["docs_enabled"] else None,
        "redoc": "/redoc" if env_info["docs_enabled"] else None,
        "health": "/health",
        "debug": env_info["debug_mode"]
    }

# Route d'informations sur l'environnement
@app.get("/environment")
async def environment_info():
    """
    Informations sur l'environnement actuel
    """
    return get_environment_info()


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
    # Configuration par défaut si lancé directement
    uvicorn.run(
        "main:app",
        host=getattr(settings, 'host', '127.0.0.1'),
        port=getattr(settings, 'port', 8000),
        reload=getattr(settings, 'reload', True),
        log_level=settings.log_level.lower()
    ) 