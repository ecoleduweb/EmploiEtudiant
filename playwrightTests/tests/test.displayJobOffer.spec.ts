import { test, expect } from '@playwright/test';

test.describe('diplayJobOffer', () => {

    test.beforeEach(async ({ page }) => {
        // se connecte au site (ADDRESSE A CHANGER LORSQUE LE SITE SERA DÉPLOYÉ)
        await page.goto('http://localhost:5173/emplois');
        await page.waitForLoadState('networkidle');
        if (await page.locator("#cookieBannerOk")) {
            await page.locator("#cookieBannerOk").click()
        }
    });

    test('Afficher les offres', async ({ page }) => {

        await page.getByText('EMPLOIS').click();
        await page.getByText('DISPONIBLES').click();
        await page.getByRole('button', { name: 'Stagiaire en Génie Logiciel 1' }).click();
        await page.getByRole('button', { name: 'Stagiaire en Génie Logiciel 1' }).nth(1).click();
        await page.getByRole('button', { name: 'close', exact: true }).click();
        await page.getByRole('button', { name: 'Stagiaire en Génie Logiciel 1' }).click();
        await expect(page.getByText('Type de poste')).toBeVisible();
        await expect(page.getByText('Adresse du lieu de travail')).toBeVisible();
        await expect(page.getByText('Description du poste')).toBeVisible();
        await expect(page.getByText('Date de début')).toBeVisible();
        await expect(page.getByText('Date limite pour postuler')).toBeVisible();
        await expect(page.getByText('Où envoyer votre candidature')).toBeVisible();
    });
})