import { test, expect } from '@playwright/test';
import { cityMocks } from '../Helper/Mocks/city.mock';
import { enterpriseMocks } from '../Helper/Mocks/enterprise.mock';
import { ApiMocker } from '../Helper/mockApi';

test.describe('Enterprise Management', () => {
    let apiMocker: ApiMocker;

    test.beforeEach(async ({ page }) => {
        apiMocker = new ApiMocker(page);

        // Mock de base pour toutes les entreprises
        await apiMocker.addMocks([
            cityMocks.success,
            enterpriseMocks.all,
        ]).apply();

        await page.goto('http://localhost:5002/enterprise');
        await page.waitForLoadState('networkidle');

        if (await page.locator("#cookieBannerOk").isVisible()) {
            await page.locator("#cookieBannerOk").click();
        }
    });

    test('Affichage de la liste des entreprises', async ({ page }) => {
        // Vérifier que les entreprises sont affichées
        await expect(page.getByText('Entreprise Test 1')).toBeVisible();
        await expect(page.getByText('Entreprise Test 2')).toBeVisible();
        await expect(page.getByText('Montreal Solutions')).toBeVisible();
    });

    test('Recherche d\'entreprise par nom', async ({ page }) => {
        // Rechercher par nom
        await page.getByPlaceholder('Rechercher une entreprise...').fill('Montreal');

        // Vérifie que seule l'entreprise correspondante est visible
        await expect(page.getByText('Montreal Solutions')).toBeVisible();
        await expect(page.getByText('Entreprise Test 1')).not.toBeVisible();
        await expect(page.getByText('Entreprise Test 2')).not.toBeVisible();
    });

    test('Recherche d\'entreprise par email', async ({ page }) => {
        await page.getByPlaceholder('Rechercher une entreprise...').fill('test1@example.com');

        await expect(page.getByText('Entreprise Test 1')).toBeVisible();
        await expect(page.getByText('Entreprise Test 2')).not.toBeVisible();
        await expect(page.getByText('Montreal Solutions')).not.toBeVisible();
    });

    test('Recherche d\'entreprise par téléphone', async ({ page }) => {
        await page.getByPlaceholder('Rechercher une entreprise...').fill('5145553333');

        await expect(page.getByText('Montreal Solutions')).toBeVisible();
        await expect(page.getByText('Entreprise Test 1')).not.toBeVisible();
    });

    test('Recherche d\'entreprise par adresse', async ({ page }) => {
        await page.getByPlaceholder('Rechercher une entreprise...').fill('Blvd');

        await expect(page.getByText('Montreal Solutions')).toBeVisible();
        await expect(page.getByText('Entreprise Test 1')).not.toBeVisible();
    });

    test('Réinitialisation de la recherche', async ({ page }) => {
        // Faire une recherche
        await page.getByPlaceholder('Rechercher une entreprise...').fill('Montreal');
        await expect(page.getByText('Entreprise Test 1')).not.toBeVisible();

        // Effacer la recherche
        await page.getByPlaceholder('Rechercher une entreprise...').clear();

        // Toutes les entreprises doivent réapparaître
        await expect(page.getByText('Entreprise Test 1')).toBeVisible();
        await expect(page.getByText('Entreprise Test 2')).toBeVisible();
        await expect(page.getByText('Montreal Solutions')).toBeVisible();
    });

    test('Création d\'une nouvelle entreprise', async ({ page }) => {
        // Mock pour la création
        await apiMocker.addMocks([
            enterpriseMocks.createNew
        ]).apply();

        // Cliquer sur le bouton de création
        await page.getByRole('button', { name: 'Créer une nouvelle entreprise' }).click();

        // Attendre que la modale s'ouvre
        await expect(page.locator('.modal')).toBeVisible();

        // Remplir le formulaire
        await page.locator('#enterprise-name').fill('Nouvelle Entreprise');
        await page.locator('#enterprise-email').fill('nouvelle@example.com');
        await page.locator('#enterprise-phone').fill('4185554444');
        await page.locator('#enterprise-address').fill('321 Rue Nouvelle');

        // Sélectionner une ville
        await page.locator('#enterprise-city').click();
        await page.getByRole('option', { name: 'Abercorn' }).click();

        // Soumettre
        await page.locator('.modal').getByRole('button', { name: 'Créer' }).click();

        // Vérifier que la modale se ferme
        await expect(page.locator('.modal')).not.toBeVisible();
    });

    test('Validation du formulaire de création - champs vides', async ({ page }) => {
        await page.getByRole('button', { name: 'Créer une nouvelle entreprise' }).click();

        // Essayer de soumettre sans remplir
        await page.locator('.modal').getByRole('button', { name: 'Créer' }).click();

        // Vérifier que les erreurs s'affichent
        await expect(page.getByText('Vous devez nommer votre entreprise')).toBeVisible();
        await expect(page.getByText('Vous devez ajouter une adresse à votre entreprise')).toBeVisible();
        await expect(page.getByText('Votre entreprise doit avoir un courriel')).toBeVisible();
        await expect(page.getByText('Vous devez mettre un numéro de téléphone à votre entreprise')).toBeVisible();
        await expect(page.getByText('Vous devez mettre une ville à votre entreprise')).toBeVisible();
    });

    test('Validation du formulaire - email invalide', async ({ page }) => {
        await page.getByRole('button', { name: 'Créer une nouvelle entreprise' }).click();

        await page.locator('#enterprise-name').fill('Test');
        await page.locator('#enterprise-email').fill('email-invalide');

        await page.locator('.modal').getByRole('button', { name: 'Créer' }).click();

        await expect(page.getByText('Le courriel doit être valide')).toBeVisible();
    });

    test('Modification d\'une entreprise existante', async ({ page }) => {
        // Mock pour la modification
        await apiMocker.addMocks([
            enterpriseMocks.update
        ]).apply();

        // Cliquer sur le bouton d'édition de la première entreprise
        await page.locator('.enterprise').first().click();

        // Attendre que la modale s'ouvre
        await expect(page.locator('.modal')).toBeVisible();

        // Modifier le nom
        await page.locator('#enterprise-name').clear();
        await page.locator('#enterprise-name').fill('Entreprise Modifiée');

        // Modifier l'email
        await page.locator('#enterprise-email').clear();
        await page.locator('#enterprise-email').fill('modifie@example.com');

        // Soumettre
        await page.locator('.modal').getByRole('button', { name: 'Modifier' }).click();

        // Vérifier que la modale se ferme
        await expect(page.locator('.modal')).not.toBeVisible();
    });
});
