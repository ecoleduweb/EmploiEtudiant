# API

## Developing

### Prerequisites
Se mettre dans le répertoire /API
```bash
pip install -r requirements.txt
```

### Setting up the environment variables
Créer un .env dans le répertoire /API avec les variables suivantes:
```env
DATABASE_TEST_URL= url de la base de données de test
BEARER_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IeyJlbWFpbCI6InBoaWxzYXVjaWVyQGdtYWlsLmNvbSIsImV4cCI6MTcxMDnNk6hD83xlj9

DATABASE_DEV_URL= url de la base de données de développement
CORS=http://localhost

SECRET_KEY=clé secrète
RECAPTCHA_KEY="myPrivateCaptchaKey"

MAIL_PORT = Port du Serveur SMTP (habituellement 587)
MAIL_ADMINISTRATOR_ADDRESS = L'adresse qui recevra les alertes de créations d'offre d'emplois, de modification de celles-ci, etc
MAIL_SERVER = URL du serveur SMTP
MAIL_SENDER = Destinateur du courriel
MAIL_SERVER_LOGIN = Courriel de Login sur le serveur SMTP
MAIL_SERVER_PASSWORD = Mot de passe de Login sur le serveur SMTP
```

### Mise en place de la Base de Données

# Créer la base de données de test avec ce script:

```sql
CREATE DATABASE H2024;
USE H2024;
```
Prendre le script de création de la BD à `/back-end/scriptBD.sql` et l'exécuter, ensuite créer un utilisateur admin et lui ajouter les accès:
```sql
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON H2024test.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
```

### Setting migration

## To set the database for the first time
1. Créer la Base de données selon les étapes du dernier point
2. Instancier le dossier de migration (s'il n'existe pas déjà)
```bash
flask db init (to initialise the database)
```

3. Effectuer une migration
```bash
flask db migrate -m "Nom_Migration"
flask db upgrade
```
4. Delete the version of alembic in the database
```sql
DELETE FROM alembic_version;
```
5. Restore the previous migration folder
6. Upgrade with the previous database
```bash
flask db upgrade
```

## Résumé des commandes:
```bash
flask db init (Pour instancier les migrations dès la première utilisation)
flask db migrate -m "Nom_de_la_migration" (cree une nouvelle migration)
flask db upgrade (pour update les changements)
flask db downgrade (pour revenir en arriere)
flask db history (voir toutes les migration)
flask db branches (Afficher les points de branchement actuels)
```

### Logging
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

### Starting the server
```bash
flask db upgrade (pour update les changements)
flask run
```

#### Starting the server if "flask run" is broken
```bash
python -m flask run
```

#### Starting the server on all the network
```bash
flask run --host=0.0.0.0
```

### Running the tests

Lancer les tests avec la commande:
```bash
pytest
```
