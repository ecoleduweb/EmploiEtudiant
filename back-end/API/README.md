# API

## Mise en place
Se mettre dans le répertoire /API

### Logiciels
Python (s'assurer d'avoir le python dans le path)

### Requis

```bash
pip install -r requirements.txt
```

### Setting up the environment variables
Voir les variables dans le fichier .env.template et y mettre les bonnes valeurs.

### To set the database for the first time
```sql
CREATE DATABASE H2024;
USE H2024;
```
Prendre le script de création de la BD à `/back-end/scriptBD.sql` et l'exécuter, ensuite créer un utilisateur admin et lui ajouter les accès.
Note : Il est aussi possible d'utiliser root en développement local.
```sql
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON H2024.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
```
Finalement, rouler les migrations
`flask db upgrade`

## Comment effectuer une migration
Falsk utilise alembic. L'idée ici est d'y aller code first. Ça implique donc que lorsqu'on modifie le modèle dans le code en python, on peut écrire une suite de commandes pour mettre à jour la bd.

1. Mettre à jour le modèle en python
2. Créer la migration
```bash
flask db migrate -m "Nom_Migration"
flask db upgrade
```

## Comment fonctionne les tests?

Simplement écrire la commande `pytest`.

## Logging
Import logger:
```
from logging import getLogger
logger = getLogger(__name__)
```

Error levels:
- Info
- Warning
- Error
- Critical

```
logger.info("message")
logger.warning("message")
logger.error("message")
logger.critical("message")
```

## Starting the server
```bash
flask db upgrade (pour update les changements)
flask run
```
