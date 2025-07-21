# 🔧 Guide des Environnements Multiples

Cette API supporte plusieurs environnements distincts avec des configurations spécialisées.

## 🚀 Démarrage Rapide

### 1. Configuration Automatique (Recommandé)

```bash
# Configurer l'environnement de développement
python3 scripts/setup_env.py dev

# Lancer en mode développement
./dev
```

### 2. Configuration Manuelle

```bash
# Copier le fichier d'exemple
cp config/env.dev.example config/.env.dev

# Lancer directement
./dev
```

## 🏗️ Environnements Disponibles

### 🔧 Développement (`development`)

**Caractéristiques :**
- **Port :** 8000
- **Host :** 127.0.0.1
- **Debug :** Activé
- **Reload :** Automatique
- **Documentation :** Swagger + ReDoc activés
- **CORS :** Ouvert pour localhost
- **Logs :** Niveau DEBUG

**Configuration :**
```bash
python3 scripts/setup_env.py dev
./dev
```

**URLs :**
- API : http://127.0.0.1:8000
- Documentation : http://127.0.0.1:8000/docs
- ReDoc : http://127.0.0.1:8000/redoc

### 🏭 Production (`production`)

**Caractéristiques :**
- **Port :** 80
- **Host :** 0.0.0.0
- **Debug :** Désactivé
- **Reload :** Désactivé
- **Documentation :** Désactivée pour la sécurité
- **CORS :** Restreint aux domaines autorisés
- **Logs :** Niveau WARNING
- **Workers :** Multiple (4)

**Configuration :**
```bash
python3 scripts/setup_env.py prod
# Éditer config/.env.prod pour configurer BDD et domaines
python3 scripts/start_prod.py
```

### 🧪 Test (`test`)

**Caractéristiques :**
- **Port :** Variable
- **Debug :** Activé
- **Tokens :** Expiration rapide (5 min)
- **Pagination :** Réduite pour les tests

**Configuration :**
```bash
python3 setup_env.py test
pytest
```

## 📊 Gestion des Environnements

### Statut des Environnements

```bash
# Afficher le statut de tous les environnements
python3 setup_env.py
```

### Changement d'Environnement

```bash
# Par variable d'environnement
export ENVIRONMENT=production
python3 main.py

# Par script dédié (recommandé)
python3 start_prod.py
```

### Informations Runtime

```bash
# API endpoint pour les infos d'environnement
curl http://localhost:8000/environment
```

## 🔐 Sécurité par Environnement

### Développement
- Clés secrètes simples
- CORS ouvert
- Logs détaillés
- Documentation accessible

### Production
- ⚠️ **Clés secrètes générées automatiquement**
- ⚠️ **CORS restreint** - Configurez vos domaines !
- ⚠️ **Documentation désactivée**
- Logs minimaux pour les performances

## 🗄️ Configuration Base de Données

### Ports par Environnement

- **Développement :** Port 5433 (`pms_incendie_dev`)
- **Production :** Port 5432 (`pms_incendie_prod`)
- **Test :** Port 5434 (`pms_incendie_test`)

### Setup PostgreSQL Local

```bash
# Démarrer plusieurs instances PostgreSQL
docker run -d --name postgres-dev -p 5433:5432 -e POSTGRES_DB=pms_incendie_dev postgres:15
docker run -d --name postgres-prod -p 5432:5432 -e POSTGRES_DB=pms_incendie_prod postgres:15
docker run -d --name postgres-test -p 5434:5432 -e POSTGRES_DB=pms_incendie_test postgres:15
```

## 📁 Structure des Dossiers

```
project/
├── .env.dev          # Config développement
├── .env.prod         # Config production  
├── .env.test         # Config test
├── env.*.example     # Templates
├── uploads/
│   ├── dev/         # Fichiers développement
│   ├── prod/        # Fichiers production
│   └── test/        # Fichiers test
├── start_dev.py     # Launcher développement
├── start_prod.py    # Launcher production
└── setup_env.py     # Configuration assistant
```

## 🚀 Scripts de Lancement

### Développement
```bash
python3 start_dev.py
```

### Production
```bash
python3 start_prod.py
```

### Flexible
```bash
ENVIRONMENT=development python3 main.py
```

## 🧪 Tests

```bash
# Configurer l'environnement de test
python3 setup_env.py test

# Lancer les tests
ENVIRONMENT=test pytest

# Tests avec coverage
ENVIRONMENT=test pytest --cov=.
```

## 🔧 Dépannage

### Problème : Environnement non reconnu
```bash
# Vérifier l'environnement actuel
python3 -c "from config import get_environment; print(get_environment())"
```

### Problème : Configuration manquante
```bash
# Reconfigurer un environnement
python3 setup_env.py dev  # Force la recreation
```

### Problème : Base de données inaccessible
```bash
# Vérifier la connectivité
python3 -c "from config import settings; print(settings.database_url)"
```

## 📝 Variables d'Environnement

### Variables Communes
- `ENVIRONMENT` : Type d'environnement
- `DATABASE_URL` : Connexion PostgreSQL
- `SECRET_KEY` : Clé JWT
- `DEBUG` : Mode debug
- `LOG_LEVEL` : Niveau de logs

### Variables Spécifiques Production
- `CORS_ORIGINS` : Domaines autorisés
- `ENABLE_DOCS` : Activer la documentation
- `UPLOAD_DIR` : Dossier d'upload sécurisé

## 🔗 Intégration CI/CD

### GitHub Actions
```yaml
env:
  ENVIRONMENT: test
steps:
  - run: python3 setup_env.py test
  - run: python3 -m pytest
```

### Docker
```dockerfile
ENV ENVIRONMENT=production
COPY .env.prod .env.prod
CMD ["python3", "start_prod.py"]
```

## 💡 Bonnes Pratiques

1. **Développement** : Utilisez toujours `start_dev.py`
2. **Production** : Vérifiez `.env.prod` avant le déploiement
3. **Sécurité** : Ne committez jamais les fichiers `.env.*`
4. **Tests** : Isolez avec l'environnement test
5. **Monitoring** : Consultez `/environment` pour le debug

---

🔥 **Environnements prêts pour le développement et la production !** 