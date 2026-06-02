import { test, expect } from '@playwright/test';
import { cityMocks } from '../Helper/Mocks/city.mock';
import { enterpriseMocks } from '../Helper/Mocks/enterprise.mock';
import { ApiMocker } from '../Helper/mockApi';
import { userMocks } from '../Helper/Mocks/user.mock';

const BASE_URL = 'http://localhost:5002';
const CITY_CACHE = {
    cities: [
        { label: 'Abercorn', value: 1 },
        { label: 'Ville Test 2', value: 2 },
        { label: 'Montreal', value: 3 },
    ],
    cachingDate: 1,
};

const openCreateEnterpriseModal = async (page: any) => {
    const openButton = page.getByRole('button', {
        name: 'Créer une nouvelle entreprise',
    });
    const modal = page.locator('.modal');
    await expect(openButton).toBeVisible();
    await openButton.click();
    if (!(await modal.isVisible())) {
        await openButton.click();
    }
    await expect(modal).toBeVisible();
};



test.describe('Enterprise Management', () => {
    let apiMocker: ApiMocker;

    test.beforeEach(async ({ page }) => {
        apiMocker = new ApiMocker(page);

        await apiMocker.addMocks([
            userMocks.all,
            userMocks.meModerator,
            cityMocks.success,
            enterpriseMocks.all,
            enterpriseMocks.notFoundEmployerEnterprise,
        ]).apply();

        await page.addInitScript((value: string) => {
            localStorage.setItem('City', value);
        }, JSON.stringify(CITY_CACHE));
        await page.addInitScript(() => {
            localStorage.setItem('cookieConsent', 'accepted');
        });

        await page.goto(`${BASE_URL}/enterprise`);
        await expect(page.getByPlaceholder('Rechercher une entreprise...')).toBeVisible();
        await expect(page.getByText('Entreprise Test 1')).toBeVisible();
    });

    test('Affichage de la liste des entreprises', async ({ page }) => {
        await expect(page.getByText('Entreprise Test 1')).toBeVisible();
        await expect(page.getByText('Entreprise Test 2')).toBeVisible();
        await expect(page.getByText('Montreal Solutions')).toBeVisible();
    });

    test('Recherche d\'entreprise par nom', async ({ page }) => {
        await page.getByPlaceholder('Rechercher une entreprise...').fill('Montreal');

        await expect(page.getByText('Montreal Solutions')).toBeVisible();
        await expect(page.getByText('Entreprise Test 2')).toBeVisible();
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
        await page.getByPlaceholder('Rechercher une entreprise...').fill('Montreal');
        await expect(page.getByText('Entreprise Test 1')).not.toBeVisible();

        await page.getByPlaceholder('Rechercher une entreprise...').clear();

        await expect(page.getByText('Entreprise Test 1')).toBeVisible();
        await expect(page.getByText('Entreprise Test 2')).toBeVisible();
        await expect(page.getByText('Montreal Solutions')).toBeVisible();
    });

    test('Création d\'une nouvelle entreprise', async ({ page }) => {
        // Mock pour la création
        await apiMocker.addMocks([
            enterpriseMocks.createNew
        ]).apply();
        await expect(page.getByText('Entreprise Test 1')).toBeVisible();
        // Cliquer sur le bouton de création
        await openCreateEnterpriseModal(page);

        // Remplir le formulaire
        await page.locator('#enterprise-name').fill('Nouvelle Entreprise');
        await page.locator('#enterprise-email').fill('nouvelle@example.com');
        await page.locator('#enterprise-phone').fill('4185554444');
        await page.locator('#enterprise-address').fill('321 Rue Nouvelle');

        // Sélectionner une ville
        await page.locator('#enterprise-city').click();
        await page.getByRole('option', { name: 'Abercorn' }).click();
        await page.locator('#enterprise-user').click();
        await page.getByRole('option', { name: 'John1 Doe1 (John1@gmail.com)' }).click();

        // Soumettre
        await page.locator('.modal').getByRole('button', { name: 'Envoyer' }).click();

        // Vérifier que la modale se ferme
        await expect(page.locator('.modal')).not.toBeVisible();

        // Vérifier que la nouvelle entreprise apparaît dans la liste
        await expect(
            page.locator('.enterprise').getByText('Nouvelle Entreprise')
        ).toBeVisible();
    });

    test('Validation du formulaire - champs vides', async ({ page }) => {
        await openCreateEnterpriseModal(page);
        await page.locator('.modal').getByRole('button', { name: 'Envoyer' }).click();

        await expect(page.getByText('Le nom de l\'entreprise est requis')).toBeVisible();
        await expect(page.getByText('L\'adresse de l\'entreprise doit être au minimum 3 caractères')).toBeVisible();
        await expect(page.getByText('Le courriel doit être de 4 caractères minimum')).toBeVisible();
        await expect(page.getByText('Le numéro de téléphone est requis')).toBeVisible();
        await expect(page.getByText('Vous devez mettre une ville à votre entreprise')).toBeVisible();
    });

    test('Validation du formulaire - email invalide', async ({ page }) => {
        await openCreateEnterpriseModal(page);
        await page.locator('#enterprise-name').fill('Test');
        await page.locator('#enterprise-email').fill('email-invalide');
        await page.locator('.modal').getByRole('button', { name: 'Envoyer' }).click();

        await expect(page.getByText('Le courriel doit être valide')).toBeVisible();
    });

    test('Modification d\'une entreprise', async ({ page }) => {
        await apiMocker.addMocks([enterpriseMocks.update]).apply();

        await page.locator('.enterprise').first().click();
        await expect(page.locator('.modal')).toBeVisible();

        await page.locator('#enterprise-name').clear();
        await page.locator('#enterprise-name').fill('Entreprise Modifiée');
        await page.locator('#enterprise-email').clear();
        await page.locator('#enterprise-email').fill('modifie@example.com');

        await page.locator('.modal').getByRole('button', { name: 'Envoyer' }).click();

        await expect(page.locator('.modal')).not.toBeVisible();
    });
});

test.describe('City Management', () => {
    let apiMocker: ApiMocker;

    test.beforeEach(async ({ page }) => {
        apiMocker = new ApiMocker(page);

        await apiMocker.addMocks([
            cityMocks.success,
            enterpriseMocks.all
        ]).apply();

        await page.addInitScript((value: string) => {
            localStorage.setItem('City', value);
        }, JSON.stringify(CITY_CACHE));
        await page.addInitScript(() => {
            localStorage.setItem('cookieConsent', 'accepted');
        });

        await page.goto(`${BASE_URL}/enterprise`);
        await expect(page.getByPlaceholder('Rechercher une entreprise...')).toBeVisible();
        await expect(page.getByText('Entreprise Test 1')).toBeVisible();
    });

    test('Vérifier que la nouvelle ville a été ajoutée à la liste', async ({ page }) => {
        await apiMocker.addMocks([enterpriseMocks.createNew]).apply();
        await openCreateEnterpriseModal(page);

        await page.locator('#enterprise-name').fill('Nouvelle Entreprise');
        await page.locator('#enterprise-email').fill('nouvelle@example.com');
        await page.locator('#enterprise-phone').fill('4185554444');
        await page.locator('#enterprise-address').fill('321 Rue Nouvelle');

        await page.locator('#enterprise-city').click();
        await page.getByRole('option', { name: 'Abercorn' }).click();
        await page.keyboard.press('Escape');

        await page.locator('.modal').getByRole('button', { name: 'Envoyer' }).click();
        await expect(page.locator('.modal')).not.toBeVisible();

        await expect(
            page.locator('.enterprise').getByText('Nouvelle Entreprise', { exact: true })
        ).toBeVisible();
        const newEnterpriseRow = page
            .locator('.enterprise')
            .filter({ hasText: 'Nouvelle Entreprise' });
        await expect(newEnterpriseRow.getByText('Abercorn', { exact: true })).toBeVisible();
    });

    test('Valider que la ville a bien changé lors de la modification', async ({ page }) => {
        await apiMocker.addMocks([enterpriseMocks.update]).apply();

        await page.locator('.enterprise').first().click();
        await expect(page.locator('.modal')).toBeVisible();

        await page.locator('.modal').getByRole('button', { name: 'Envoyer' }).click();
        await expect(page.locator('.modal')).not.toBeVisible();

        await expect(page.getByText('Moncton')).toBeVisible();
    });
});

