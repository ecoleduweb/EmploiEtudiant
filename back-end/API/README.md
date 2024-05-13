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
```
### Setting migration
```bash
flask db init
flask db migrate -m "Nom_de_la_migration"(cree une nouvelle migration)
flask db upgrade (pour update les changements)
flask db downgrade (pour revenir en arriere)
flask db history (voir toutes les migration)
flask db branches (Afficher les points de branchement actuels)
```
### To set the database for the first time
1. Wipe the /migrations folder
2. Create the Database
```sql
CREATE DATABASE H2024
```
3. Create your migration folder
```bash
flask db init (to initialise the database)
```
4. Do the migration 
```bash
flask db migrate -m "Nom_Migration"
flask db upgrade
```
5. Delete the version of alembic in the database
```sql
DELETE FROM alembic_version;
```
6. Restore the previous migration folder
7. Upgrade with the previous database
```bash
flask db upgrade
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

### Routes
#### /user
- /createUser
    - POST
    - Créer un utilisateur
    - Token requis
    - Paramètres:
        - email: string
        - password: string

- /login
    - POST
    - Se connecter
    - Paramètres:
        - email: string
        - password: string

- /updatePassword
    - PUT
    - Mettre à jour le mot de passe
    - Token requis
    - Paramètres:
        - email: string
        - password: string

- /getUser
    - GET
    - Récupérer un utilisateur
    - Token requis
    - Paramètres:
        - email: string

- /getAllUsers
    - GET
    - Récupérer tous les utilisateurs
    - Token requis

#### /jobOffer

- /offreEmploi/:id
    - GET
    - Récupérer une offre d'emploi selon l'id
    - Paramètres:
        - id: int

- /offresEmploi
    - GET
    - Récupérer toutes les offres d'emploi


### Running the tests

Créer la base de données de test avec ce script:
```sql
CREATE DATABASE H2024test;
USE H2024test;
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) DEFAULT FALSE,
    active BOOLEAN DEFAULT FALSE,
    isModerator BOOLEAN DEFAULT FALSE
);
CREATE TABLE IF NOT EXISTS job_offer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    dateEntryOffice DATETIME NOT NULL,
    deadlineApply DATE NOT NULL,
    email VARCHAR(255) NOT NULL,
    hoursPerWeek FLOAT NOT NULL,
    compliantEmploymentStandards BOOLEAN NOT NULL,
    internship BOOLEAN NOT NULL,
    offerStatus INT NOT NULL,
    offerLink VARCHAR(255) NOT NULL,
    urgent BOOLEAN NOT NULL,
    active BOOLEAN NOT NULL,
    employerId INT NOT NULL,
    scheduleId INT NOT NULL
);

CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON H2024test.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
```
Pour les tests, mettre un token valide dans le .env

Lancer les tests avec la commande:
```bash
pytest
```
