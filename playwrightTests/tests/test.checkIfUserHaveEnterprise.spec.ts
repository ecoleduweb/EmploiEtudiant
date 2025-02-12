import { test, expect } from '@playwright/test';
import { studyProgramMocks } from '.././Helper/Mocks/studyProgram.mock';
import { ApiMocker } from '.././Helper/mockApi';
import { enterpriseMocks } from '../Helper/Mocks/enterprise.mock';
import { loginMocks } from '../Helper/Mocks/login.mock';



test.describe('checkIfUserHaveEnterprise', () => {

    test.beforeAll(async ({ page }) => {
        const apiMocker = new ApiMocker(page);
        await apiMocker.addMocks([
            studyProgramMocks.success,
            loginMocks.success])
            .apply();

        // se connecte au site (ADDRESSE A CHANGER LORSQUE LE SITE SERA DÉPLOYÉ)
        await page.goto('http://localhost:5002/login');
        await page.getByLabel('Nom d\'utilisateur').fill('test@gmail.com');
        await page.getByLabel('Mot de passe').fill('test');
        await page.getByRole('button', { name: 'Se connecter' }).click();
    });

    test('hasEntreprise', async ({ page }) => {
        const apiMocker = new ApiMocker(page);
        await apiMocker.addMock(
            enterpriseMocks.success)
            .apply();

        await page.goto('http://localhost:5002/dashboard');
        await page.waitForLoadState('networkidle');
        if (await page.locator("#cookieBannerOk")) {
            await page.locator("#cookieBannerOk").click()
        }
        await expect(page.locator("#editEnterprise")).toBeVisible();
        await page.goto('http://localhost:5002/profile');
        await page.waitForLoadState('networkidle');
        await expect(page.locator("#editEnterprise")).toBeVisible();
    });

    test('newUserWithoutEnterprise', async ({ page }) => {
        const apiMocker = new ApiMocker(page);
        await apiMocker.addMock(
            enterpriseMocks.notFound)
            .apply();

        await page.goto('http://localhost:5002/dashboard');
        await page.waitForLoadState('networkidle');
        if (await page.locator("#cookieBannerOk")) {
            await page.locator("#cookieBannerOk").click()
        }

        await expect(page.locator("#editEnterprise")).toBeHidden();
        await page.goto('http://localhost:5002/profile');
        await page.waitForLoadState('networkidle');
        await expect(page.locator("#editEnterprise")).toBeHidden();
    });
});