# PMS Protection Incendie - API Backend

API de gestion de projet pour une entreprise de fabrication et d'installation de réseaux de protection incendie.

## 🚀 Fonctionnalités

- **Gestion des projets** : Création, suivi et gestion complète des projets d'installation
- **Ressources humaines** : Gestion des employés, tâches et assignations
- **Parc véhicules** : Suivi des véhicules, kilométrages et conducteurs
- **Matériel** : Inventaire et gestion du matériel
- **Produits & Stock** : Gestion des produits, articles et mouvements de stock
- **Fabrication** : Ordres de fabrication et nomenclatures (BOM)
- **Finance** : Grand livre, comptabilité et caisses de projet
- **Documents** : Upload, stockage et gestion des documents
- **Logistique** : Livraisons et approvisionnements

## 📋 Prérequis

- Python 3.8+
- PostgreSQL 15+
- pip ou pipenv

## 🛠️ Installation

### 1. Cloner le projet
```bash
git clone <repo-url>
cd pms-efficience
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration de la base de données

Créer une base de données PostgreSQL :
```sql
CREATE DATABASE pms_incendie;
CREATE USER pms_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE pms_incendie TO pms_user;
```

### 5. Configuration de l'environnement

Copier le fichier d'exemple et le modifier :
```bash
cp .env.example .env
```

Éditer le fichier `.env` avec vos paramètres :
```bash
DATABASE_URL=postgresql://pms_user:your_password@localhost:5432/pms_incendie
SECRET_KEY=your-super-secret-key-here
```

### 6. Initialiser la base de données

Les tables seront créées automatiquement au démarrage de l'application grâce à SQLAlchemy.

Alternativement, vous pouvez exécuter le script SQL directement :
```bash
psql -U pms_user -d pms_incendie -f schema_bdd.sql
```

## 🚀 Démarrage

### Mode développement
```bash
python main.py
```

### Avec uvicorn
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible sur : http://localhost:8000

## 📚 Documentation

### Documentation interactive
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

### Endpoints principaux

#### Authentification
- `POST /auth/login` - Connexion
- `POST /auth/refresh` - Renouvellement de token
- `POST /auth/register` - Inscription (admin)

#### Santé de l'API
- `GET /health` - Vérification de l'état de l'API
- `GET /` - Informations générales

#### Données de référence
- `GET /api/v1/devise` - Liste des devises
- `GET /api/v1/expense-categories` - Catégories de dépenses
- `GET /api/v1/statuts/*` - Différents statuts

#### Documents
- `POST /api/v1/documents` - Upload de fichier
- `GET /api/v1/documents/{id}` - Métadonnées document
- `DELETE /api/v1/documents/{id}` - Suppression

## 🔐 Authentification

L'API utilise JWT (JSON Web Tokens) pour l'authentification.

### Test de connexion
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123"
  }'
```

### Utilisation du token
```bash
curl -X GET "http://localhost:8000/api/v1/devise" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 📁 Structure du projet

```
pms-efficience/
├── main.py                 # Point d'entrée FastAPI
├── config.py               # Configuration
├── database.py             # Configuration base de données
├── auth.py                 # Authentification JWT
├── dependencies.py         # Dépendances communes
├── requirements.txt        # Dépendances Python
├── .env.example           # Exemple de configuration
├── schema_bdd.sql         # Schéma de base de données
├── routes.md              # Documentation des routes
├── models/                # Modèles SQLAlchemy ORM
│   ├── __init__.py
│   ├── base.py
│   ├── referentiels.py
│   ├── documents.py
│   ├── hr.py
│   ├── vehicles.py
│   ├── materials.py
│   ├── products.py
│   ├── projects.py
│   ├── manufacturing.py
│   ├── finance.py
│   └── logistics.py
├── schemas/               # Schémas Pydantic
│   ├── __init__.py
│   ├── common.py
│   ├── auth.py
│   ├── referentiels.py
│   ├── documents.py
│   ├── hr.py
│   ├── vehicles.py
│   ├── materials.py
│   ├── products.py
│   ├── projects.py
│   ├── manufacturing.py
│   ├── finance.py
│   └── logistics.py
└── routes/                # Endpoints API
    ├── __init__.py
    ├── auth.py
    ├── common.py
    ├── referentiels.py
    └── documents.py
```

## 🧪 Tests

Pour lancer les tests :
```bash
pytest
```

## 🔧 Développement

### Ajout d'un nouvel endpoint

1. Créer le modèle SQLAlchemy dans `models/`
2. Créer les schémas Pydantic dans `schemas/`
3. Créer les routes dans `routes/`
4. Ajouter le routeur dans `main.py`

### Migration de base de données

Si vous modifiez les modèles, vous pouvez utiliser Alembic pour les migrations :
```bash
alembic init alembic
alembic revision --autogenerate -m "Description du changement"
alembic upgrade head
```

## 📝 Notes importantes

- Tous les endpoints (sauf `/health` et `/`) nécessitent une authentification
- Les fichiers uploadés sont stockés dans le dossier `uploads/`
- La pagination par défaut est de 20 éléments par page
- Les timestamps sont en UTC
- La suppression par défaut est "soft delete"

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalité`)
3. Commit les changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalité`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence [À définir].

## 📞 Support

Pour toute question ou problème, contactez l'équipe de développement. 