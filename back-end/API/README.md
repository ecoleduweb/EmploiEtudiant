# API

### Logiciels

Python (s'assurer d'avoir le python dans le path)

### Requis

Dans le dossier back-end

```bash
pip install -r requirements.txt
```
Mes notes :
Dans mon fichier requirements.txt, le paquet mariadb==1.1.10 doit être retiré lorsque j'exécute le projet sous Windows, car ce module n’est pas compatible avec Python 3.14 sur Windows.
Ce module nécessite la présence du MariaDB Connector/C, un composant natif qui doit être installé séparément, et qui n’est pas détecté automatiquement sous Windows avec Python 3.14.
Comme alternative, j’utilise pymysql, une bibliothèque 100% Python, qui ne nécessite aucune compilation ni dépendance native.
pymysql est pleinement compatible avec MariaDB, car MariaDB utilise le protocole MySQL.

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
Mes notes :
On doit se positioner dans API/app/_init.py c'est la ou se trouve la creation de l'app avec FLASK 
flask --app app:create_app db upgrade
Ou comme ca peut savoir Flask methode qui permet d ecreer l'applciaiton  ensuit eon fait les upgrade dans base donne 


Finalement, rouler les migrations
`flask db upgrade`

note : Si flaks n'est pas installé en global, tu peux utiliser
`python -m flask db upgrade`

### Demarre l'app

`flask run --debug` debug permet de redémarrer l'application quand on modifie le code.
Mes note:
Quand je fais comme ce script ca lance mais ca redirige vers la route / qui est vide donc je dosi toujours apres lurl 1127...:5000/route comme /ping ou une autre route 
et ensuite pour tester avec post avec methode post :
curl -X POST http://127.0.0.1:5000/user/login `
     -H "Content-Type: application/json" `
     -d '{"email":"test@gmail.com","password":"phil123"}'


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
  Ensuite activer naviguer vers Scripts :

```bash
  cd myenv\Scripts\
```
   Activer l'environnement
```bash
  .\Activate.ps1
```
  Reinstaller les packages requirements.txt :
```bash
  pip install -r requirements.txt
```
Pour desactiver votre environnement utiliser la commande :

```bash
  deactivate
```
Note : Pour utiliser l'environnement vous devrez l'activer(```.\Activate.ps1```) à chaque fois et ne pas oublier de le desactiver quand vous avez fini

