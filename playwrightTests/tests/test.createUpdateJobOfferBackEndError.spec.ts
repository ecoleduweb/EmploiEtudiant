import { test, expect } from './fixtures';
import { studyProgramMocks } from '.././Helper/Mocks/studyProgram.mock';
import { cityMocks } from '.././Helper/Mocks/city.mock';
import { employmentScheduleMocks } from '.././Helper/Mocks/employmentSchedule.mock';
import { jobOfferMocks } from '.././Helper/Mocks/jobOffer.mock';
import { ApiMocker } from '.././Helper/mockApi';
import { enterpriseMocks } from '../Helper/Mocks/enterprise.mock';
import { loginMocks } from '../Helper/Mocks/login.mock';
import { userMocks } from '../Helper/Mocks/user.mock';


test.describe('createUpdateJobOfferBackEndError', () => {
  let apiMocker: any;
  test.beforeEach(async ({ page }) => {
    apiMocker = new ApiMocker(page);
    await apiMocker.addMocks([
      studyProgramMocks.success,
      cityMocks.success,
      employmentScheduleMocks.success,
      jobOfferMocks.jobOfferNew,
      userMocks.meUser,
      enterpriseMocks.success,
    ])
      .apply();
  });

  test('Nouvelle offre invalide', async ({ page }) => {
    await apiMocker.addMocks([jobOfferMocks.emptyJobOfferEmployer]).apply();
    await apiMocker.addMocks([jobOfferMocks.jobOfferNewInvalid]).apply();
    await apiMocker.addMocks([jobOfferMocks.jobOfferVerifyURL]).apply();

    await page.goto('http://localhost:5002/dashboard');
    await page.waitForLoadState('networkidle');
    if (await page.locator("#cookieBannerOk")) {
      await page.locator("#cookieBannerOk").click()
    }

    await page.getByRole('button', { name: 'Créer une nouvelle offre' }).click();

    // JobOffer
    await page.locator('#title').first().click();
    await page.locator('#title').first().fill('Poste');

    await page.getByPlaceholder('Choisir période(s)').click();
    await page.getByRole('option', { name: 'temps plein' }).click();

    await page.locator('#address').first().click();
    await page.locator('#address').first().fill('Addresse 123');

    await page.getByPlaceholder('Choisir programme(s)').first().click();
    await page.getByRole('option', { name: 'Arts visuels' }).click();

    await page.getByLabel('Salaire Horaire').click();
    await page.getByLabel('Salaire Horaire').fill('32');

    await page.getByLabel('Heures/semaine*').click();
    await page.getByLabel('Heures/semaine*').fill('40');

    await page.getByLabel('Lien vers l\'offre d\'emploi détaillée').click();
    await page.getByLabel('Lien vers l\'offre d\'emploi détaillée').fill('https://google.ca');

    await page.locator('#email').first().click();
    await page.locator('#email').first().fill('test@gmail.com');

    // [contenteditable="true"] représente le rich text editor de la description de l'offre
    await page.locator('[contenteditable="true"]').click();
    await page.keyboard.type('Test description');

    await page.getByLabel('J\'accepte les conditions*').check();
    await page.getByRole('button', { name: 'Envoyer' }).click();

    await expect(page.getByText('Ceci est un retour pour tester les erreurs back-end pour ajouter.')).toBeVisible();
  });

  test.skip('Update offre invalide', async ({ page }) => {
    await apiMocker.addMocks([jobOfferMocks.jobOfferNewOffer]).apply();
    await apiMocker.addMocks([jobOfferMocks.jobOfferUpdateInvalid]).apply();
    await apiMocker.addMocks([loginMocks.success]).apply();
    await apiMocker.addMocks([userMocks.meUser]).apply();
    await apiMocker.addMocks([enterpriseMocks.hasCurrentEnterprise]).apply();
    await apiMocker.addMocks([jobOfferMocks.jobOfferVerifyURL]).apply();

    await page.goto('http://localhost:5002/login');
    await page.waitForLoadState('networkidle');
    await page.getByLabel('Nom d\'utilisateur').fill('test@gmail.com');
    await page.getByLabel('Mot de passe').fill('test');
    await page.getByRole('button', { name: 'Se connecter' }).click();

    await page.goto('http://localhost:5002/dashboard');
    await page.waitForLoadState('networkidle');
    if (await page.locator("#cookieBannerOk")) {
      await page.locator("#cookieBannerOk").click()
    }

    await page.locator('button.button.edit').first().click();

    // JobOffer
    await page.locator('#title').first().click();
    await page.locator('#title').first().fill('poste');

    await page.locator('#address').first().click();
    await page.locator('#address').first().fill('Addresse 123');

    await page.locator('label[for="programme"] ').first().click();
    await page.getByRole('option', { name: 'Arts visuels' }).click();

    await page.getByLabel('Salaire Horaire').click();
    await page.getByLabel('Salaire Horaire').fill('32');

    await page.getByLabel('Heures/semaine*').click();
    await page.getByLabel('Heures/semaine*').fill('40');

    await page.getByLabel('Lien vers l\'offre d\'emploi détaillée').click();
    await page.getByLabel('Lien vers l\'offre d\'emploi détaillée').fill('https://google.ca');

    await page.locator('#email').first().click();
    await page.locator('#email').first().fill('test@gmail.com');

    // [contenteditable="true"] représente le rich text editor de la description de l'offre
    await page.locator('[contenteditable="true"]').click();
    await page.keyboard.type('Test description');

    await page.getByLabel('J\'accepte les conditions*').check();
    await page.getByRole('button', { name: 'Envoyer' }).click();

    await expect(await page.getByText('Ceci est un retour pour tester les erreurs back-end pour modifier.')).toBeVisible();
  });

});