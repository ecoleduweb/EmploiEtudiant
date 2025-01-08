# Déamarrage à neuf d'un serveur pour le projet

Ce readme explique comment configurer le serveur, suite à un démarrage à neuf.

## 1. Exécuter le script install.sh

Ce script installe et configure les éléments suivants:

- unattended-upgrades
- nodejs 20.11.1
- python 3.12
- mariadb-server
- nginx
- UFW (A 22,443, 80)

## 2. Configurer les services
### Front-end
Exécutez la commande suivante
```bash
sudo systemctl --force --full edit front-end.service
```
Insérez les valeurs suivantes dans le fichier qui s'ouvre
```bash
[Unit]
Description=Front end
After=network.target

[Service]
WorkingDirectory=/root/dev_project/ProjetApplicationH2024/front-end/projet_application
ExecStart=/usr/bin/node -r dotenv/config ./build/index.js
User=root

[Install]
WantedBy=multi-user.target
```
Activez le service avec la commande suivante:
```bash
sudo systemctl enable front-end
```

### Back-end
Exécutez la commande suivante
```bash
sudo systemctl --force --full edit back-end.service
```
Insérez les valeurs suivantes dans le fichier qui s'ouvre
```bash
[Unit]
Description=My Flask API service
After=network.target

[Install]
WantedBy=multi-user.target
[Service]
Type=simple
User=root
PermissionsStartOnly=true
WorkingDirectory=/root/dev_project/ProjetApplicationH2024/back-end/API
ExecStart=gunicorn -b 0.0.0.0:5000 app:create_app()
Restart=on-failure
TimeoutSec=600
```
Activez le service avec la commande suivante:
```bash
sudo systemctl enable back-end
```
L'action github va se charger de démarrer les services lorsque nécéssaire.

## 3 Configuration de la base de données

### Création de la base de données
Pour se connecter au service mariadb, exécutez la commande suivante:
```bash
mysql --no-defaults
```
Une fois dans mariadb, exécutez la commande suivante pour créer la base de données:
```sql
CREATE DATABASE H2024;
```

### Création de l'utilisateur de la DB
Une fois dans mariadb, exécutez la commande suivante pour créer l'utilisateur:
```sql
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'CHANGEZ_CE_MOT_DE_PASSE';
GRANT ALL PRIVILEGES ON H2024.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
```
(La valeur CHANGEZ_CE_MOT_DE_PASSE doit être elle utilisée par l'application)

## 4 Suite à cette étape, assurez vous de configurer le PROXY NGINX. Une documentation sur celui-ci est disponible dans la branche [proxy-server](https://github.com/ecoleduweb/ProjetApplicationH2024/blob/proxy-server/README.md).

## 5 Configurez les GitHub Actions pour déployer automatiquement sur le serveur.
[Documentation DigitalOcean](https://medium.com/swlh/how-to-deploy-your-application-to-digital-ocean-using-github-actions-and-save-up-on-ci-cd-costs-74b7315facc2)
