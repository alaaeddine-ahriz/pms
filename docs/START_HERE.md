# 🚀 Guide de Démarrage - API PMS Protection Incendie

## 📋 Prérequis

1. **Python 3.8+** (recommandé: Python 3.12 avec pyenv)
2. **PostgreSQL** (optionnel - SQLite disponible pour tests)
3. **Git** pour cloner le projet

## ⚡ Démarrage Ultra-Rapide (2 minutes)

### 1. Test Immédiat - Sans Configuration

```bash
# Lance l'API avec SQLite (aucune config requise)
./no-db
```

✅ **Avantages** : Zéro configuration, test immédiat
📱 **Accès** : http://127.0.0.1:8000/docs

### 2. Développement Complet

```bash
# Configuration automatique
python3 scripts/setup_env.py dev

# Vérification
python3 scripts/check_setup.py

# Lancement
./dev
```

## 🎯 **Structure du Projet**

```
pms-efficience/
├── 📋 docs/                    # 📖 Toute la documentation
│   ├── START_HERE.md          # 🚀 Ce guide
│   ├── STRUCTURE.md           # 📁 Organisation du projet  
│   ├── DB_SETUP.md           # 🗄️ Configuration base de données
│   └── ENVIRONMENTS.md       # ⚙️ Gestion environnements
│
├── 🚀 scripts/                # 🛠️ Scripts utilitaires
│   ├── start_dev.py          # 🔧 Lancement développement
│   ├── start_no_db.py        # 🧪 Lancement sans PostgreSQL  
│   ├── start_prod.py         # 🏭 Lancement production
│   ├── setup_env.py          # ⚙️ Configuration environnements
│   ├── check_setup.py        # 🔍 Vérification configuration
│   └── activate_env.sh       # 🐍 Activation environnement Python
│
├── ⚙️ config/                  # 📝 Configuration
│   ├── env.*.example         # 📋 Templates configuration
│   ├── .env.dev              # 🔧 Config développement (généré)
│   ├── docker-compose.dev.yml # 🐳 PostgreSQL via Docker
│   └── swagger_config.py     # 📖 Configuration Swagger UI
│
├── 🧪 tests/                  # 🧪 Tests et exemples
│   ├── test_api.py           # 🧪 Tests API
│   └── swagger_demo.py       # 🎨 Démonstration Swagger
│
├── 🚀 Raccourcis             # ⚡ Lancement rapide
│   ├── dev                   # ./dev = développement
│   └── no-db                 # ./no-db = sans PostgreSQL
│
└── 🔧 Core                   # 💾 Fichiers principaux
    ├── main.py              # 🌐 Point d'entrée FastAPI
    ├── config.py            # ⚙️ Configuration multi-environnements
    ├── models/             # 🏗️ Modèles SQLAlchemy
    ├── routes/             # 🌐 Routes FastAPI
    └── schemas/            # 📝 Schémas Pydantic
```

## 🔧 **Configuration Détaillée**

### **Étape 1: Environnement Python**

#### Option A: Avec pyenv (Recommandé)
```bash
# Installer Python 3.12
pyenv install 3.12

# Créer environnement virtuel
pyenv virtualenv 3.12 venv-3.12

# Activer
pyenv activate venv-3.12

# Ou utiliser le script automatique
source scripts/activate_env.sh
```

#### Option B: Python système
```bash
# Vérifier la version
python3 --version  # Minimum 3.8

# Installer les dépendances
pip install -r requirements.txt
```

### **Étape 2: Configuration Environnement**

```bash
# Configuration automatique
python3 scripts/setup_env.py dev

# Vérification complète
python3 scripts/check_setup.py
```

### **Étape 3: Base de Données** 

#### Option A: Sans PostgreSQL (Rapide)
```bash
# Utilise SQLite automatiquement
./no-db
```

#### Option B: PostgreSQL avec Docker (Recommandé)
```bash
# Démarrer PostgreSQL
docker-compose -f config/docker-compose.dev.yml up -d

# Vérifier que c'est actif
docker ps

# Lancer l'API
./dev
```

#### Option C: PostgreSQL Local (macOS)
```bash
# Installer
brew install postgresql@15
brew services start postgresql@15

# Créer la base
createdb pms_incendie_dev

# Configurer l'utilisateur (optionnel)
psql -d pms_incendie_dev -c "CREATE USER dev_user WITH PASSWORD 'dev_password';"

# Lancer l'API
./dev
```

## 🌐 **Accès à l'API**

Une fois lancée, l'API est accessible sur :

| Service | URL | Description |
|---------|-----|-------------|
| **API** | http://127.0.0.1:8000 | Point d'entrée principal |
| **Swagger** | http://127.0.0.1:8000/docs | Documentation interactive |
| **ReDoc** | http://127.0.0.1:8000/redoc | Documentation alternative |
| **Health** | http://127.0.0.1:8000/health | Santé de l'API |
| **Environment** | http://127.0.0.1:8000/environment | Infos environnement |

## 🔐 **Test d'Authentification**

```bash
# Connexion (utilisateur de test)
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password123"}'

# Réponse attendue
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}

# Utilisation du token
curl -H "Authorization: Bearer <token>" \
  http://127.0.0.1:8000/api/v1/projects
```

## 🛠️ **Scripts Pratiques**

| Commande | Usage | Description |
|----------|-------|-------------|
| `./dev` | **Développement quotidien** | PostgreSQL + hot reload |
| `./no-db` | **Test rapide** | SQLite + démarrage immédiat |
| `python3 scripts/setup_env.py dev` | **Première fois** | Configuration environnement |
| `python3 scripts/check_setup.py` | **Diagnostic** | Vérification complète |

## 🧪 **Modes de Fonctionnement**

### **Mode Développement** (`./dev`)
```bash
# Caractéristiques
✅ Port 8000
✅ Hot reload automatique  
✅ Documentation Swagger activée
✅ Logs détaillés (DEBUG)
✅ CORS ouvert pour localhost
✅ PostgreSQL (port 5433)
```

### **Mode Test Rapide** (`./no-db`)
```bash
# Caractéristiques  
✅ Port 8000
✅ SQLite temporaire
✅ Documentation Swagger activée
✅ Aucune configuration requise
⚠️ Données perdues au redémarrage
```

### **Mode Production** (`scripts/start_prod.py`)
```bash
# Caractéristiques
✅ Port 80 (nécessite sudo)
❌ Documentation désactivée
❌ Hot reload désactivé
✅ Logs minimaux (WARNING)
✅ CORS restreint
✅ Plusieurs workers
```

## 🔧 **Dépannage**

### **Problème: Python/Pyenv**
```bash
# Installer pyenv (macOS)
brew install pyenv

# Configuration shell (.zshrc)
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Redémarrer le terminal
```

### **Problème: PostgreSQL**
```bash
# Vérifier si PostgreSQL écoute
lsof -i :5433

# Redémarrer PostgreSQL (macOS)
brew services restart postgresql@15

# Voir les logs Docker
docker logs postgres-dev
```

### **Problème: Port occupé**
```bash
# Trouver le processus sur port 8000
lsof -i :8000

# Arrêter le processus
kill -9 <PID>
```

### **Problème: Import/Module**
```bash
# Vérifier l'environnement Python
python3 -c "import sys; print(sys.path)"

# Réinstaller les dépendances
pip install -r requirements.txt
```

## 📖 **Guides Spécialisés**

| Guide | Quand l'utiliser |
|-------|------------------|
| **[📁 STRUCTURE.md](STRUCTURE.md)** | Comprendre l'organisation |
| **[🗄️ DB_SETUP.md](DB_SETUP.md)** | Problèmes de base de données |
| **[⚙️ ENVIRONMENTS.md](ENVIRONMENTS.md)** | Configuration avancée |

## 🎯 **Prochaines Étapes**

1. **✅ Démarrage réussi** - API accessible sur http://127.0.0.1:8000/docs
2. **🔐 Test authentification** - Connexion avec admin@example.com  
3. **📖 Explorer l'API** - Swagger UI interactif
4. **🏗️ Développement** - Ajouter vos fonctionnalités
5. **🚀 Déploiement** - Configuration production

---

🔥 **Vous êtes prêt à développer !**

Pour toute question : consultez les autres guides dans `docs/` ou utilisez `python3 scripts/check_setup.py` 