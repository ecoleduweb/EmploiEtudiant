# Guide d'utilisation des tests Playwright

## Introduction

Playwright est un framework de test front-end qui permet d'automatiser les tests sur différents navigateurs (Chrome, Firefox, Safari). Ce guide vous aidera à comprendre comment utiliser Playwright pour vos tests.

## Prérequis

- Node.js (version 14 ou supérieure)
- npm ou yarn
- Extension Visual Studio "Playwright Test for VSCode"

## Structure d'un test de base

Voici un exemple de test Playwright simple :

```javascript
// example.spec.js
import { test, expect } from '@playwright/test';

test('titre de mon test', async ({ page }) => {
    // Naviguer vers une URL
    await page.goto('http://localhost:5002/login');
    
    // Vérifie si le titre de la page est présent
    await expect(page.getByText('Authentification')).toBeVisible();
});
```

## Éléments clés de Playwright
### 1. Les objets de test

Playwright utilise des "objets de test" pour injecter des contextes :

- `page` : Une page de navigateur unique
- `browser` : L'instance du navigateur
- `context` : Le contexte du navigateur

Dans notre cas, nous utilisons majoritairement `page`.

### 2. Les vérifications

Playwright utilise `expect` pour les vérifications :

```javascript
// Vérifier un texte sur la page
await expect(page.locator('h1')).toHaveText('Bienvenue');

// Vérifier qu'un élément est visible
await expect(page.locator('.login-button')).toBeVisible();
```

`Expect` fait ce qu'il dit, il s'attend à voir ce qu'on lui donne. Si il ne le trouve pas, le test échoue et si il le trouve le test est validé.

### 3. Les sélecteurs

Playwright offre plusieurs façons de sélectionner des éléments :

```javascript
// Premier élément correspondant
page.locator('#titre').first();

// Deuxième élément correspondant (index 1)
page.locator('#titre').nth(1);

// Par CSS
page.locator('.submit-button');

// Par texte (moins utilisé dans notre cas)
page.locator('text=Connexion');

// Par attribut (moins utilisé dans notre cas)
page.locator('[data-test="login-button"]');
```

## Exécution des tests

Assurez vous que l'application roule en local avant de démarrer les tests.

### Via l'extension VS Code

1. Ouvrez la vue "Testing" dans VS Code (icône de fiole dans la barre de gauche)
2. Vous verrez tous les tests Playwright listés
3. Options d'exécution :
    - Cliquez sur le bouton "Run Test" à côté d'un test pour l'exécuter individuellement
    - Cliquez sur "Run Tests" pour exécuter tous les tests
    - Utilisez "Debug Tests" pour lancer un test en mode débogage

Si vous voulez vois les test travailler en temps réel sur un navigateur WEB, ouvrez la section "PLAYWRIGHT" et cochez "Show browser". La prochaine fois que vous executez les tests, chromium devrait s'ouvrir.

### Via la ligne de commande

Il est toujours possible d'exécuter les tests depuis le terminal (c'est préférable d'utiliser l'extension) :

```bash
# Exécuter tous les tests
npx playwright test

# Exécuter un fichier de test spécifique
npx playwright test tests/montest.spec.js

# Exécuter en mode débogage
npx playwright test --debug

# Exécuter les tests dans un navigateur spécifique
npx playwright test --project=chromium
```

## Débogage

Si vous avez besoin de déboguer un test :

```javascript
// Ajouter une pause dans le test
await page.pause();

// Ou exécuter en mode debug
// npx playwright test --debug
```

## Rapports de test

Playwright génère automatiquement des rapports après l'exécution des tests. Vous pouvez les consulter de deux façons :

### Via l'extension VS Code

1. Après avoir exécuté vos tests, l'extension affiche un lien "Show Report" en haut de la vue Testing
2. Cliquez sur ce lien pour ouvrir le rapport HTML dans votre navigateur par défaut
3. Le rapport affiche tous les tests, leur statut, durée et captures d'écran en cas d'échec

### Via ligne de commande

```bash
npx playwright show-report
```

Les rapports Playwright permettent de voir en détail les étapes exécutées, les erreurs rencontrées et les captures d'écran pour faciliter le débogage.

## Mocks

Les tests utilisent des "mocks" pour simuler les calls au back-end. Nous pouvons choisir ce que nous voulons dépendant ce que nous avons besoin de tester.

### Création d'un mock

Dans le dossier Mocks, plusieurs éxistent déjà. Voici un le Mock qui simule le call "studyPrograms" : 

```javascript
import { MockConfig } from "../types";
// Déclaration du mock
export const studyProgramMocks = {
    // Quand l'api retourne "success"
    success: {
        // L'url du call à l'api
        url: '*/**/studyProgram/studyPrograms',
        // La réponse de l'api
        response: {
            status: 200,
            json: [{
                "id": 9,
                "name": "Arts visuels"
            }]
        }
    },
    //Quand l'api retourne "notFound"
    notFound: {
        // L'url du call à l'api
        url: '*/**/studyProgram/studyPrograms',
        // La réponse de l'api
        response: {
            status: 404,
            json: {
                message: "Pas de programme d'études trouvé"
            }
        }
    }
} satisfies Record<string, MockConfig>;
```

studyPrograms nous permet normalement d'aller chercher une liste de programme d'étude. Dans cet exemple, nous déclarons "studyProgramMocks" avec "success" et "notFound". "success" et "notFound" représente les retours différents que l'api peut avoir. Par exemple, "success" va retourne le code 200 avec un programme d'étude.

### Utilisation des mocks

Pour utiliser un mock, nous le déclarons au début du test. Voici un exemple : 

```javascript
// example.spec.js
import { test, expect } from '@playwright/test';
import { studyProgramMocks } from '.././Helper/Mocks/studyProgram.mock';

test('titre de mon test', async ({ page }) => {
    // Déclaration du mock
    const apiMocker = new ApiMocker(page);
        await apiMocker.addMocks([
            studyProgramMocks.success])
            .apply();

    // Naviguer vers une URL
    await page.goto('http://localhost:5002/login');
    
    // Vérifie si le titre de la page est présent
    await expect(page.getByText('Authentification')).toBeVisible();
});
```

Si nous voulons utiliser un ou plusieurs mocks pour tous les tests, nous pouvons faire un beforeEach qui va s'éxécuter avant chaque test : 

```javascript
test.beforeEach(async ({ page }) => {
        const apiMocker = new ApiMocker(page);
        await apiMocker.addMocks([
            studyProgramMocks.success,
            loginMocks.success])
            .apply();
});

test('test1', async ({ page }) => {
    // le premier test ...
});

test('test2', async ({ page }) => {
    // le deuxième test ...
});        
```

Une fois les mocks déclarés, la prochaine fois que le front-end fait un appel à ce mock, la valeur retourné va être ce qui est déclaré sur le mock.

## Exemple complet

```javascript
import { test, expect } from '@playwright/test';
import { studyProgramMocks } from '.././Helper/Mocks/studyProgram.mock';
import { ApiMocker } from '.././Helper/mockApi';
import { loginMocks } from '../Helper/Mocks/login.mock';

test.describe('testDeLogin', () => {

    test.beforeEach(async ({ page }) => {
        // On déclare les mocks nécéssaires
        const apiMocker = new ApiMocker(page);
        await apiMocker.addMocks([
            studyProgramMocks.success,
            ])
            .apply();
            
        // On se déplace sur la page de login
        await page.goto('http://localhost:5002/login');
        // On attends que la page se charge
        await page.waitForLoadState('networkidle');
    });

    // On déclare le premier test
    test('loginEnterprise', async ({ page }) => {
        // On déclare un mock unique à ce test
        const apiMocker = new ApiMocker(page);
        await apiMocker.addMock(
            loginMocks.success)
            .apply();

        // On remplit le champ "Nom d'utilisateur" par la donnée que nous voulons
        await page.getByLabel('Nom d\'utilisateur').fill('test@gmail.com');
        // On remplit le champ "Mot de passe" par la donnée que nous voulons
        await page.getByLabel('Mot de passe').fill('test');
        // On appui sur le boutton "Se connecter"
        await page.getByRole('button', { name: 'Se connecter' }).click();

        await page.goto('http://localhost:5002/dashboard');
        await page.waitForLoadState('networkidle');

        // On s'attend à voir ce texte sur la page dashboard
        // Puisque nous avons déclaré loginMocks.succes, l'utilisateur est connecté et devrait être 
        // capable de voir ses offres.
        await expect(page.getByText('MES OFFRES D\'EMPLOIS')).toBeVisible();
    });

    //autres tests ...
});
```

## Documentation

Ce guide vous donne les bases pour commencer avec Playwright. N'hésitez pas à consulter la [documentation officielle](https://playwright.dev/docs/intro) pour des informations plus détaillées.