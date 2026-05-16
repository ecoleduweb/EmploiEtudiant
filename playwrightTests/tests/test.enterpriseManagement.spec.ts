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
            cityMocks.success,
            enterpriseMocks.all,
            userMocks.meModerator,
            userMocks.all
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
        await expect(page.getByText('Entreprise Test 1')).not.toBeVisible();
    });

    test('Recherche d\'entreprise par email', async ({ page }) => {
        await page.getByPlaceholder('Rechercher une entreprise...').fill('test1@example.com');
        await expect(page.getByText('Entreprise Test 1')).toBeVisible();
        await expect(page.getByText('Entreprise Test 2')).not.toBeVisible();
    });

    test('Validation du formulaire - champs vides', async ({ page }) => {
        await openCreateEnterpriseModal(page);
        await page.locator('.modal').getByRole('button', { name: 'Créer' }).click();

        await expect(page.getByText('Vous devez nommer votre entreprise')).toBeVisible();
        await expect(page.getByText('Vous devez mettre une ville à votre entreprise')).toBeVisible();
    });

    
});
test.describe('Enterprise Création', () => {
    let apiMocker: ApiMocker;

    test.beforeEach(async ({ page }) => {
        apiMocker = new ApiMocker(page);

        await apiMocker.addMocks([
            cityMocks.success,
             enterpriseMocks.allWithNew,
            userMocks.meModerator,
            userMocks.all
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

  

 test("Création d'une entreprise avec employés", async ({ page }) => {
    await apiMocker.addMocks([
        cityMocks.success,
        enterpriseMocks.allWithNew,
        userMocks.meModerator,
        userMocks.all
    ]).apply();

    await page.route('**/enterprise/new', async (route) => {
        await route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify(enterpriseMocks.createNew.response.json),
        });
    });

    await page.getByRole('button', { name: 'Créer une nouvelle entreprise' }).click();

    await page.locator('#enterprise-name').fill('Nouvelle Entreprise');
    await page.locator('#enterprise-address').fill('321 Rue Nouvelle');
    await page.locator('#enterprise-email').fill('nouvelle@example.com');
    await page.locator('#enterprise-phone').fill('4185554444');

    await page.locator('#enterprise-city').click();
    await page.getByRole('option', { name: 'Abercorn' }).click();
    await page.keyboard.press('Escape');

    await page.locator('#enterprise-admin').click();
    await page.getByRole('option', { name: 'Jean Employé' }).click();
    await page.keyboard.press('Escape');

    await page.locator('.modal').getByRole('button', { name: 'Créer' }).click();

    await expect(page.locator('.modal')).not.toBeVisible();


    await expect(
        page.locator('.enterprise', { hasText: 'Nouvelle Entreprise' })
    ).toBeVisible();
});

        
    
});

test.describe('Enterprise Modification', () => {
    let apiMocker: ApiMocker;

    test.beforeEach(async ({ page }) => {
        apiMocker = new ApiMocker(page);

        await apiMocker.addMocks([
            cityMocks.success,
             enterpriseMocks.allUpdated,
            userMocks.meModerator,
            userMocks.all
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

  

 test("Modification d'une entreprise", async ({ page }) => {
        await apiMocker.addMocks([
            enterpriseMocks.update,
            enterpriseMocks.allUpdated
        ]).apply();

        await page.locator('.enterprise').first().click();
        await expect(page.locator('.modal')).toBeVisible();

        await page.locator('#enterprise-name').fill('Entreprise Modifiée');
        await page.locator('#enterprise-email').fill('modifie@example.com');
        await page.locator('#enterprise-address').fill('999 Rue de la Logique');
        await page.locator('#enterprise-phone').fill('4180000000');

        await page.locator('#enterprise-city').click();
        await page.getByRole('option', { name: 'Abercorn' }).click();
        await page.keyboard.press('Escape');

        await page.locator('#enterprise-admin').click();
        await page.getByRole('option', { name: 'Marc Admin' }).click();
        await page.keyboard.press('Escape');

        await page.locator('.modal').getByRole('button', { name: 'Modifier' }).click();

        await expect(page.locator('.modal')).not.toBeVisible();

       await expect(page.getByPlaceholder('Rechercher une entreprise...')).toBeVisible();
        await expect(page.getByText('Entreprise Test 1')).toBeVisible();
    });
    
});



test.describe('City Management', () => {
    let apiMocker: ApiMocker;

    test.beforeEach(async ({ page }) => {
        apiMocker = new ApiMocker(page);
        await apiMocker.addMocks([
            cityMocks.success,
            enterpriseMocks.all,
            userMocks.meModerator,
            userMocks.all
        ]).apply();

        await page.addInitScript((value: string) => {
            localStorage.setItem('City', value);
        }, JSON.stringify(CITY_CACHE));


     
        await page.goto(`${BASE_URL}/enterprise`);
    });

    test('Vérifier que la nouvelle entreprise peut être créée', async ({ page }) => {
    await apiMocker.addMocks([
        cityMocks.success,
        userMocks.meModerator,
        userMocks.all,
        enterpriseMocks.createNew,
        enterpriseMocks.allWithNew
    ]).apply();

    await page.goto(`${BASE_URL}/enterprise`);
    await expect(page.getByPlaceholder('Rechercher une entreprise...')).toBeVisible();

    await openCreateEnterpriseModal(page);

    await page.locator('#enterprise-name').fill('Nouvelle Entreprise');
    await page.locator('#enterprise-address').fill('321 Rue Nouvelle');
    await page.locator('#enterprise-email').fill('nouvelle@example.com');
    await page.locator('#enterprise-phone').fill('4185554444');

    await page.locator('#enterprise-city').click();
    await page.getByRole('option', { name: 'Abercorn' }).click();
    await page.keyboard.press('Escape');

    await page.locator('#enterprise-admin').click();
    await page.getByRole('option', { name: 'Jean Employé' }).click();
    await page.keyboard.press('Escape');

    await page.getByRole('button', { name: 'Créer', exact: true }).click();

    await expect(page.locator('.modal')).not.toBeVisible();
    
    const row = page.locator('.enterprise').filter({ hasText: 'Nouvelle Entreprise' });
    await expect(row).toBeVisible();
    await expect(row.getByText('Abercorn')).toBeVisible();
});

    test('Valider que la ville a bien changé lors de la modification', async ({ page }) => {
        await apiMocker.addMocks([
            enterpriseMocks.update,
            enterpriseMocks.allUpdated
        ]).apply();

        await page.locator('.enterprise').first().click();
        await expect(page.locator('.modal')).toBeVisible();

        await page.locator('#enterprise-city').click();
        await page.getByRole('option', { name: 'Abercorn' }).click();
        await page.keyboard.press('Escape');

        await page.locator('.modal').getByRole('button', { name: 'Modifier' }).click();
        await expect(page.locator('.modal')).not.toBeVisible();

        await expect(page.getByText('Abercorn').first()).toBeVisible();
    });
});
