import { test, expect } from '@playwright/test';
import { studyProgramMocks } from '.././Helper/Mocks/studyProgram.mock';
import { ApiMocker } from '.././Helper/mockApi';
import { loginMocks } from '../Helper/Mocks/login.mock';
import { jobOfferMocks } from '../Helper/Mocks/jobOffer.mock';
import { userMocks } from '../Helper/Mocks/user.mock';




test.describe('checkIfOffersHide', () => {

    test.beforeEach(async ({ page }) => {
        const apiMocker = new ApiMocker(page);
        await apiMocker.addMocks([
            studyProgramMocks.success,
            loginMocks.successModerator,
            userMocks.meModerator
        ])
            .apply();
        await page.clock.install({ time: new Date('2016-02-25T08:00:00-04:00') });

        await page.goto('http://localhost:5002/login');
        await page.waitForLoadState('networkidle');
        await page.getByLabel('Nom d\'utilisateur').fill('test@gmail.com');
        await page.getByLabel('Mot de passe').fill('test');
        await page.getByRole('button', { name: 'Se connecter' }).click();
    });

    test('checkIfOffersHideAndComeBack', async ({ page }) => {
        const apiMocker = new ApiMocker(page);
        await apiMocker.addMocks([
            jobOfferMocks.jobOfferEmployerAll
        ]).apply();

        await page.goto('http://localhost:5002/dashboard');
        await page.waitForLoadState('networkidle');
        if (await page.locator("#cookieBannerOk")) {
            await page.locator("#cookieBannerOk").click()
        }


        await expect(page.locator("#refusedOffersList")).toBeVisible();
        await page.locator("#btnHideRefusedOfferList").click();
        await expect(page.locator("#refusedOffersList")).not.toBeVisible();
        await page.locator("#btnHideRefusedOfferList").click();
        await expect(page.locator("#refusedOffersList")).toBeVisible();

        await expect(page.locator("#toBeApprovedOffersList")).toBeVisible();
        await page.locator("#btnHidetoBeApprovedOfferList").click();
        await expect(page.locator("#toBeApprovedOffersList")).not.toBeVisible();
        await page.locator("#btnHidetoBeApprovedOfferList").click();
        await expect(page.locator("#toBeApprovedOffersList")).toBeVisible();

        await expect(page.locator("#offerDisplayedList")).toBeVisible();
        await page.locator("#btnHideOfferDisplayed").click();
        await expect(page.locator("#offerDisplayedList")).not.toBeVisible();
        await page.locator("#btnHideOfferDisplayed").click();
        await expect(page.locator("#offerDisplayedList")).toBeVisible();

        await expect(page.locator("#offersToComeList")).toBeVisible();
        await page.locator("#btnHideOfferToCome").click();
        await expect(page.locator("#offersToComeList")).not.toBeVisible();
        await page.locator("#btnHideOfferToCome").click();
        await expect(page.locator("#offersToComeList")).toBeVisible();

        await expect(page.locator("#expiredOfferList")).toBeVisible();
        await page.locator("#btnHideExpiredOffer").click();
        await expect(page.locator("#expiredOfferList")).not.toBeVisible();
        await page.locator("#btnHideExpiredOffer").click();
        await expect(page.locator("#expiredOfferList")).toBeVisible();


    });


});