# 📁 Structure du Projet PMS Protection Incendie

## 🎯 **Organisation Propre et Logique**

```
pms-efficience/
├── 📋 docs/                    # Documentation complète
│   ├── STRUCTURE.md            # Ce fichier
│   ├── START_HERE.md          # Guide de démarrage
│   ├── ENVIRONMENTS.md        # Configuration environnements
│   ├── DB_SETUP.md           # Configuration base de données
│   └── SUMMARY.md            # Résumé du projet
│
├── 🚀 scripts/                # Scripts de lancement et configuration
│   ├── start_dev.py          # Lancement développement
│   ├── start_no_db.py        # Lancement sans PostgreSQL
│   ├── start_prod.py         # Lancement production
│   ├── setup_env.py          # Configuration environnements
│   ├── check_setup.py        # Vérification configuration
│   └── activate_env.sh       # Activation environnement Python
│
├── ⚙️  config/                 # Fichiers de configuration
│   ├── env.dev.example       # Template développement
│   ├── env.prod.example      # Template production
│   ├── env.example           # Template générique
│   ├── .env.dev              # Config développement (généré)
│   ├── .env.prod             # Config production (généré)
│   ├── docker-compose.dev.yml # PostgreSQL via Docker
│   └── swagger_config.py     # Configuration Swagger UI
│
├── 🧪 tests/                  # Tests et exemples
│   ├── test_api.py           # Tests API
│   └── swagger_demo.py       # Démonstration Swagger
│
├── 🏗️  models/                 # Modèles SQLAlchemy
│   ├── base.py               # Base commune
│   ├── auth.py               # Authentification
│   ├── hr.py                 # Ressources humaines
│   ├── projects.py           # Projets
│   ├── finance.py            # Finance
│   ├── manufacturing.py     # Fabrication
│   ├── logistics.py          # Logistique
│   ├── materials.py          # Matériel
│   ├── products.py           # Produits & Stock
│   ├── vehicles.py           # Véhicules
│   ├── documents.py          # Documents
│   └── referentiels.py       # Données de référence
│
├── 🌐 routes/                 # Routes API FastAPI
│   ├── auth.py               # Authentification
│   ├── common.py             # Routes communes
│   ├── hr.py                 # Ressources humaines
│   ├── projects.py           # Projets
│   ├── finance.py            # Finance
│   ├── manufacturing.py     # Fabrication
│   ├── logistics.py          # Logistique
│   ├── materials.py          # Matériel
│   ├── products.py           # Produits & Stock
│   ├── vehicles.py           # Véhicules
│   ├── documents.py          # Documents
│   └── referentiels.py       # Données de référence
│
├── 📝 schemas/                # Schémas Pydantic
│   ├── common.py             # Schémas communs
│   ├── auth.py               # Authentification
│   ├── hr.py                 # Ressources humaines
│   ├── projects.py           # Projets
│   ├── finance.py            # Finance
│   ├── manufacturing.py     # Fabrication
│   ├── logistics.py          # Logistique
│   ├── materials.py          # Matériel
│   ├── products.py           # Produits & Stock
│   ├── vehicles.py           # Véhicules
│   ├── documents.py          # Documents
│   └── referentiels.py       # Données de référence
│
├── 📦 uploads/               # Fichiers uploadés (par environnement)
│   ├── dev/                 # Développement
│   ├── prod/                # Production
│   └── test/                # Tests
│
├── 🗄️ Base de Données        # Schémas et migrations
│   └── database/
│       └── init_schema.sql  # Schéma d'initialisation PostgreSQL
│
├── 🔧 Fichiers Core          # Configuration principale
│   ├── main.py              # Point d'entrée FastAPI
│   ├── config.py            # Configuration multi-environnements
│   ├── database.py          # Configuration base de données
│   ├── dependencies.py     # Dépendances FastAPI
│   ├── auth.py              # Logique authentification
│   └── requirements.txt     # Dépendances Python
│
└── 🚀 Raccourcis            # Scripts de lancement rapide
    ├── dev                  # ./dev = développement
    ├── no-db                # ./no-db = sans PostgreSQL
    └── README.md            # Documentation principale
```

## 🎯 **Avantages de cette Organisation**

### ✅ **Clarté**
- Chaque type de fichier a son dossier
- Structure intuitive et prévisible
- Séparation claire des responsabilités

### ✅ **Maintenabilité**
- Facile de trouver un fichier spécifique
- Ajout de nouvelles fonctionnalités organisé
- Configuration centralisée

### ✅ **Déploiement**
- Scripts de lancement dédiés
- Configuration par environnement
- Documentation complète

### ✅ **Développement**
- Raccourcis pratiques (`./dev`, `./no-db`)
- Tests isolés
- Configuration flexible

## 🚀 **Utilisation Pratique**

### **Démarrage Rapide**
```bash
# Ultra-rapide (sans PostgreSQL)
./no-db

# Développement complet
./dev

# Ou version longue
python3 scripts/start_dev.py
```

### **Configuration**
```bash
# Configurer un environnement
python3 scripts/setup_env.py dev

# Vérifier la configuration  
python3 scripts/check_setup.py
```

### **Base de Données**
```bash
# PostgreSQL via Docker
docker-compose -f config/docker-compose.dev.yml up -d

# Vérifier la configuration
python3 -c "from config import settings; print(settings.database_url)"
```

## 📖 **Navigation**

| Besoin | Dossier | Description |
|--------|---------|-------------|
| **Lancer l'API** | `scripts/` | Scripts de démarrage |
| **Configurer** | `config/` | Templates et configs |
| **Comprendre** | `docs/` | Documentation complète |
| **Tester** | `tests/` | Tests et exemples |
| **Développer** | `models/`, `routes/`, `schemas/` | Code métier |
| **Déboguer** | Racine | Fichiers core |

## 🔥 **Philosophie**

Cette structure suit le principe **"Convention over Configuration"** :
- **Prévisible** : Chaque type de fichier a sa place
- **Évolutive** : Facile d'ajouter de nouvelles fonctionnalités
- **Maintenable** : Structure claire pour les équipes
- **Professionnelle** : Standards de l'industrie respectés

---

🎉 **Projet maintenant organisé et professionnel !** 