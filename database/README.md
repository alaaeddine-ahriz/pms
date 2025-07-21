# 🗄️ Base de Données

Ce dossier contient tous les fichiers liés à la gestion de la base de données PostgreSQL.

## 📁 Structure

```
database/
├── README.md          # Cette documentation
└── init_schema.sql    # Schéma d'initialisation PostgreSQL
```

## 📄 Fichiers

### `init_schema.sql`
- **Rôle** : Schéma complet de la base de données PMS Incendie
- **Usage** : Exécuté automatiquement par Docker lors de l'initialisation
- **Contenu** : 
  - 30+ tables organisées en modules (RH, Projets, Finance, etc.)
  - Relations et contraintes
  - Triggers et fonctions
  - Vue matérialisée d'inventaire

### 🔄 **Utilisation avec Docker**

Le fichier est automatiquement monté dans le container PostgreSQL :

```yaml
# config/docker-compose.dev.yml
volumes:
  - ../database/init_schema.sql:/docker-entrypoint-initdb.d/schema.sql
```

**Au premier démarrage** du container, PostgreSQL exécute ce script pour créer toute la structure.

## 🛠️ **Commandes utiles**

### Réinitialiser la base (supprime toutes les données !)
```bash
docker-compose -f config/docker-compose.dev.yml down -v
docker-compose -f config/docker-compose.dev.yml up -d
```

### Appliquer le schéma manuellement
```bash
docker exec -i pms-postgres-dev psql -U dev_user -d pms_incendie_dev < database/init_schema.sql
```

### Explorer la structure
```bash
docker exec -it pms-postgres-dev psql -U dev_user -d pms_incendie_dev -c "\\dt"
```

## 🔮 **Évolutions futures**

Ce dossier pourra contenir :
- `migrations/` : Scripts de migration Alembic
- `seeds/` : Données de test/démonstration
- `backups/` : Scripts de sauvegarde
- `views/` : Vues SQL complexes 