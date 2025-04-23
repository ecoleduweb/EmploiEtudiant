# API

### Logiciels

Python (s'assurer d'avoir le python dans le path)

### Requis

Dans le dossier back-end

```bash
pip install -r requirements.txt
```

### Setting up the environment variables

Voir les variables dans le fichier .env.template et y mettre les bonnes valeurs.

### To set the database for the first time

```sql
CREATE DATABASE H2024;
CREATE DATABASE H2024TEST;
```

Prendre le script de création de la BD à `/back-end/scriptBD.sql` et l'exécuter, ensuite créer un utilisateur admin et lui ajouter les accès.
Note : Il est aussi possible d'utiliser root en développement local.

```sql
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON H2024.* TO 'admin'@'localhost';
GRANT ALL PRIVILEGES ON H2024TEST.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
```

Finalement, rouler les migrations
`flask db upgrade`

note : Si flaks n'est pas installé en global, tu peux utiliser
`python -m flask db upgrade`

### Demarre l'app

`flask run --debug` debug permet de redémarrer l'application quand on modifie le code.

Pour se connecter, utiliser les identifiants `test@gmail.com` et le mot de passe `phil123`

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

## Comment installer un environnement virtuel

- S'assurer d'être dans le dossier \back-end 
   
   Executer la commande :

```bash
  python -m venv myenv
```
  Ensuite activer l'environnement avec la commande :

```bash
  myenv\Scripts\activate
```
  Reinstaller les packages requirements.txt :
```bash
  pip install -r requirements.txt
```
Pour desactiver votre environnement utiliser la commande :

```bash
  deactivate
```
Note : Pour utiliser l'environnement vous devrez l'activer(```myenv\Scripts\activate```) à chaque fois et ne pas oublier de le desactiver quand vous avez fini

