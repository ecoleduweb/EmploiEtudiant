# 🎭 Playwright

[![npm version](https://img.shields.io/npm/v/playwright.svg)](https://www.npmjs.com/package/playwright) <!-- GEN:chromium-version-badge -->[![Chromium version](https://img.shields.io/badge/chromium-122.0.6261.29-blue.svg?logo=google-chrome)](https://www.chromium.org/Home)<!-- GEN:stop --> <!-- GEN:firefox-version-badge -->[![Firefox version](https://img.shields.io/badge/firefox-122.0-blue.svg?logo=firefoxbrowser)](https://www.mozilla.org/en-US/firefox/new/)<!-- GEN:stop --> <!-- GEN:webkit-version-badge -->[![WebKit version](https://img.shields.io/badge/webkit-17.4-blue.svg?logo=safari)](https://webkit.org/)<!-- GEN:stop -->

## [Documentation](https://playwright.dev) | [API reference](https://playwright.dev/docs/api/class-playwright)

Playwright is a framework for Web Testing and Automation. It allows testing [Chromium](https://www.chromium.org/Home), [Firefox](https://www.mozilla.org/en-US/firefox/new/) and [WebKit](https://webkit.org/) with a single API. Playwright is built to enable cross-browser web automation that is **ever-green**, **capable**, **reliable** and **fast**.

|          | Linux | macOS | Windows |
|   :---   | :---: | :---: | :---:   |
| Chromium <!-- GEN:chromium-version -->122.0.6261.29<!-- GEN:stop --> | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| WebKit <!-- GEN:webkit-version -->17.4<!-- GEN:stop --> | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Firefox <!-- GEN:firefox-version -->122.0<!-- GEN:stop --> | :white_check_mark: | :white_check_mark: | :white_check_mark: |

Headless execution is supported for all browsers on all platforms. Check out [system requirements](https://playwright.dev/docs/intro#system-requirements) for details.

Looking for Playwright for [Python](https://playwright.dev/python/docs/intro), [.NET](https://playwright.dev/dotnet/docs/intro), or [Java](https://playwright.dev/java/docs/intro)?

## Installation

La base de données utilisée est celle des tests. Elle est supprimée chaque fois qu'un test est fait.
Un utilisateur avec les accès `admin@gmail.com:test123` est créé comme administrateur pour le besoin des tests.
Un utilisateur avec les accès `user@gmail.com:test123` est créé comme employeur pour le besoin des tests.
Installer les modules npm `npm install`.

exécuter la commande  `npx playwright install`

Ajouter l'extension au module vscode : [Lien](https://marketplace.visualstudio.com/items?itemName=ms-playwright.playwright)

## Rouler les tests

Pour rouler les test, faire `npm run test`

La commande va démarrer flask et svelte et en suite rouler les tests.

## Ajouter des tests

Pour ajouter des tests, il suffit de créer un nouveau fichier dans le dossier tests et que ce fichier se termine 
par .specs.ts.

Exemple : 
```
test.exemple.specs.ts
```
Sinon Playwright ne reconnaitras pas le fichiers.

Pour ajouter un test à votre fichier, celui-ci sera créer de cette manière :

```
test('Nom du test', async ({ page }) => {
 await page.getByLabel('Nom d\'utilisateur').click();
 await page.getByLabel('Nom d\'utilisateur').fill('test@test.ca');
 // reste du test ici...
}
```

Pour obtenir la liste des actions possibles (.getByLabel, getByRole...) 

Consulter ce lien : [ICI](https://playwright.dev/docs/library)

