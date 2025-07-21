# 🗄️ Guide de Configuration Base de Données

## 🔍 **Problème** 
```
psycopg2.OperationalError: connection to server at "localhost" port 5433 failed: Connection refused
```

**Cause :** PostgreSQL n'est pas en cours d'exécution sur le port 5433.

---

## 🚀 **Solutions (par ordre de simplicité)**

### **Solution 1: Lancement Rapide SANS Base de Données**

Pour tester l'API immédiatement sans configuration :

```bash
# Lance l'API avec SQLite temporaire
./no-db
# ou: python3 scripts/start_no_db.py
```

✅ **Avantages :**
- Démarrage immédiat
- Aucune configuration requise
- Parfait pour tester l'API

⚠️ **Limitations :**
- Données temporaires (perdues au redémarrage)
- Fonctionnalités limitées

---

### **Solution 2: PostgreSQL avec Docker (Recommandé)**

#### Méthode A: Docker Compose (Simple)

```bash
# Démarrer PostgreSQL
docker-compose -f config/docker-compose.dev.yml up -d

# Vérifier que c'est lancé
docker-compose -f config/docker-compose.dev.yml ps

# Lancer l'API
./dev
```

#### Méthode B: Docker Run (Manuel)

```bash
# Démarrer Docker Desktop d'abord
open /Applications/Docker.app

# Attendre que Docker soit prêt, puis :
docker run -d \
  --name postgres-dev \
  -p 5433:5432 \
  -e POSTGRES_DB=pms_incendie_dev \
  -e POSTGRES_USER=dev_user \
  -e POSTGRES_PASSWORD=dev_password \
  postgres:15

# Vérifier
docker ps

# Lancer l'API
python3 start_dev.py
```

---

### **Solution 3: PostgreSQL Local (macOS)**

#### Installation avec Homebrew

```bash
# Installer PostgreSQL
brew install postgresql@15

# Démarrer le service
brew services start postgresql@15

# Créer la base de données
createdb pms_incendie_dev

# Créer l'utilisateur
psql -d pms_incendie_dev -c "CREATE USER dev_user WITH PASSWORD 'dev_password';"
psql -d pms_incendie_dev -c "GRANT ALL PRIVILEGES ON DATABASE pms_incendie_dev TO dev_user;"

# Modifier le port (optionnel)
# Éditer /opt/homebrew/var/postgresql@15/postgresql.conf
# port = 5433

# Redémarrer
brew services restart postgresql@15
```

#### Configuration Alternative - Port Standard

Si vous préférez utiliser le port standard 5432 :

```bash
# Modifier .env.dev
DATABASE_URL=postgresql://dev_user:dev_password@localhost:5432/pms_incendie_dev
```

---

### **Solution 4: SQLite Permanent (Développement)**

Pour éviter PostgreSQL complètement en développement :

```bash
# Modifier .env.dev
DATABASE_URL=sqlite:///./pms_dev.db
```

✅ **Avantages :**
- Aucune installation requise
- Fichier local simple
- Idéal pour le développement

⚠️ **Limitations :**
- Pas de fonctionnalités PostgreSQL avancées
- Concurrence limitée

---

## 🔧 **Vérifications et Dépannage**

### Vérifier PostgreSQL

```bash
# Vérifier si PostgreSQL écoute
lsof -i :5433

# Tester la connexion
psql -h localhost -p 5433 -U dev_user -d pms_incendie_dev

# Via Python
python3 -c "from config import settings; print(settings.database_url)"
```

### Vérifier Docker

```bash
# Statut Docker
docker --version
docker ps

# Logs du conteneur
docker logs postgres-dev

# Se connecter au conteneur
docker exec -it postgres-dev psql -U dev_user -d pms_incendie_dev
```

### Résoudre les Conflits de Port

```bash
# Trouver ce qui utilise le port 5433
lsof -i :5433

# Arrêter un processus
kill -9 <PID>

# Changer le port dans .env.dev si nécessaire
PORT=5434
```

---

## 🎯 **Recommandations par Cas d'Usage**

### **Pour Tests Rapides**
```bash
./no-db    # SQLite temporaire
```

### **Pour Développement**
```bash
docker-compose -f config/docker-compose.dev.yml up -d
./dev
```

### **Pour Production**
```bash
# PostgreSQL dédié avec sauvegarde
python3 start_prod.py
```

---

## 📋 **Commandes de Gestion Docker**

```bash
# Démarrer
docker-compose -f docker-compose.dev.yml up -d

# Arrêter
docker-compose -f docker-compose.dev.yml down

# Voir les logs
docker-compose -f docker-compose.dev.yml logs -f

# Supprimer (avec données)
docker-compose -f docker-compose.dev.yml down -v

# Redémarrer
docker-compose -f docker-compose.dev.yml restart
```

---

## 🔗 **Scripts Disponibles**

| Script | Usage | Base de Données |
|--------|-------|-----------------|
| `./no-db` | Tests rapides | SQLite temporaire |
| `./dev` | Développement | PostgreSQL (port 5433) |
| `scripts/start_prod.py` | Production | PostgreSQL (port 5432) |

---

🔥 **Choix recommandé pour commencer :**

1. **Tests immédiats** : `python3 start_no_db.py`
2. **Développement complet** : Docker + `python3 start_dev.py` 