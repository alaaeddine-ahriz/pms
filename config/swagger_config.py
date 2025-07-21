"""
Configuration avancée pour Swagger UI
Personnalisation de l'interface et des métadonnées
"""

# Configuration des tags pour organiser la documentation
SWAGGER_TAGS = [
    {
        "name": "Authentication",
        "description": "🔐 **Authentification JWT**\n\nGestion des tokens d'accès et authentification des utilisateurs.",
        "externalDocs": {
            "description": "En savoir plus sur JWT",
            "url": "https://jwt.io/",
        },
    },
    {
        "name": "Common",
        "description": "🏥 **Endpoints communs**\n\nPoints de contrôle de santé et utilitaires généraux.",
    },
    {
        "name": "Reference Data", 
        "description": "📋 **Données de référence**\n\nDevises, statuts, catégories et autres données de base du système.",
    },
    {
        "name": "Documents",
        "description": "📁 **Gestion documentaire**\n\nUpload, stockage et organisation des documents avec système de tags.",
    },
    {
        "name": "Human Resources",
        "description": "👥 **Ressources Humaines**\n\nGestion des employés, tâches, assignations et suivi des équipes.",
    },
    {
        "name": "Vehicles",
        "description": "🚗 **Parc automobile**\n\nGestion des véhicules, relevés kilométriques et assignation des conducteurs.",
    },
    {
        "name": "Materials",
        "description": "🔧 **Matériel et équipements**\n\nInventaire du matériel, factures et documentation associée.",
    },
    {
        "name": "Products & Stock",
        "description": "📦 **Gestion des stocks**\n\nProduits, articles, mouvements de stock et inventaire en temps réel.",
    },
    {
        "name": "Projects",
        "description": "🏗️ **Gestion de projets**\n\nProjets, sites clients, caisses et allocation des ressources.",
    },
    {
        "name": "Manufacturing",
        "description": "🏭 **Fabrication**\n\nOrdres de fabrication, nomenclatures (BOM) et suivi de production.",
    },
    {
        "name": "Finance",
        "description": "💰 **Finance et comptabilité**\n\nGrand livre, comptes, écritures comptables et rapports financiers.",
    },
    {
        "name": "Logistics",
        "description": "🚚 **Logistique**\n\nLivraisons, approvisionnements et suivi des demandes.",
    },
]

# Description enrichie de l'API
API_DESCRIPTION = """
## 🔥 API PMS Protection Incendie

### 🎯 Vue d'ensemble
API complète pour la gestion d'une entreprise spécialisée dans les systèmes de protection incendie.
Couvre tous les aspects métier : projets, RH, stocks, fabrication, finance et logistique.

---

### 🔐 Authentification Quick Start

**1. Connexion :**
```bash
POST /auth/login
{
  "email": "admin@example.com", 
  "password": "password123"
}
```

**2. Utilisation du token :**
```bash
Authorization: Bearer <votre_token>
```

**3. Test en une ligne :**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password123"}'
```

---

### 📊 Fonctionnalités Principales

| Module | Fonctionnalités | Endpoints |
|--------|----------------|-----------|
| **🏗️ Projets** | Sites clients, équipes, caisses | `/api/v1/projects/*` |
| **👥 RH** | Employés, tâches, assignations | `/api/v1/employees/*` |
| **📦 Stock** | Mouvements, inventaire temps réel | `/api/v1/stocks/*` |
| **🏭 Fabrication** | Ordres, BOM, suivi photos | `/api/v1/bom/*` |
| **💰 Finance** | Grand livre, comptabilité | `/api/v1/ledger/*` |
| **🚚 Logistique** | Livraisons, approvisionnements | `/api/v1/deliveries/*` |

---

### 🎨 Conventions API

- **Pagination** : `?page=1&page_size=20`
- **Filtrage** : `?q=recherche&date_from=2024-01-01`
- **Soft Delete** : `DELETE /resource/{id}?force=true`
- **Idempotence** : Header `Idempotency-Key`

---

### 🚀 Démarrage Rapide

1. **Installation** : `pip install -r requirements.txt`
2. **Configuration** : Copier `.env.example` → `.env`
3. **Initialisation** : `python3 quick_start.py`
4. **Démarrage** : `python3 main.py`

---

### 🔗 Liens Utiles

- 📖 **Documentation technique** : `README.md`
- 🧪 **Tests API** : `python3 test_api.py`
- 🚀 **Demo Swagger** : `python3 swagger_demo.py`
- 🌐 **ReDoc** : [`/redoc`](/redoc)

---

### 💡 Support

Pour toute question ou support technique :
- 📧 Email : alaaahriz@gmail.com
- 📋 Issues : [GitHub Repository](#)
- 📞 Assistance : +212 XXX XXX XXX
"""

# Configuration des réponses d'exemple
EXAMPLE_RESPONSES = {
    "authentication_success": {
        "description": "Connexion réussie",
        "content": {
            "application/json": {
                "example": {
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "token_type": "bearer",
                    "expires_in": 1800
                }
            }
        }
    },
    "validation_error": {
        "description": "Erreur de validation",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "loc": ["body", "email"],
                            "msg": "field required",
                            "type": "value_error.missing"
                        }
                    ]
                }
            }
        }
    }
}

# Configuration Swagger UI avancée
SWAGGER_UI_PARAMETERS = {
    "deepLinking": True,
    "displayRequestDuration": True,
    "docExpansion": "none",
    "operationsSorter": "method",
    "filter": True,
    "showExtensions": True,
    "showCommonExtensions": True,
    "tryItOutEnabled": True
}

# CSS personnalisé pour Swagger UI
CUSTOM_SWAGGER_CSS = """
<style>
.swagger-ui .topbar { display: none }
.swagger-ui .info .title { color: #d32f2f }
.swagger-ui .scheme-container { background: #fafafa; border: 1px solid #d32f2f }
</style>
""" 