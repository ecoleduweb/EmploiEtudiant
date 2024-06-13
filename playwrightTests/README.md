# 🎭 Playwright

## Installation

La base de données utilisée est celle des tests. Elle est supprimée chaque fois qu'un test est fait.
Un utilisateur avec les accès `admin@gmail.com:test123` est créé comme administrateur pour le besoin des tests.
Un utilisateur avec les accès `user@gmail.com:test123` est créé comme employeur pour le besoin des tests.
Une ville nommée `ville` est aussi créée.
Installer les modules npm `npm install`.

exécuter la commande  `npx playwright install`

Ajouter l'extension au module vscode : [Lien](https://marketplace.visualstudio.com/items?itemName=ms-playwright.playwright)

## Rouler les tests automatiquement

Pour rouler les test, faire `npm run test`

La commande va démarrer flask et svelte et en suite rouler les tests.

## Ajouter des tests

### Installation
Ajouter l'extension playwright à visual studio code

### Ajout
- Cliquer sur le bouton Record new
- Pour ajouter dans un fichier, faire Record at cursor.

### Teardown

En bas, dans les options, il y a globalteardown pour supprimer les instances des serveurs spawnées. À utiliser avant certains tests (register) ou si on fait des changements dans le serveur flask.