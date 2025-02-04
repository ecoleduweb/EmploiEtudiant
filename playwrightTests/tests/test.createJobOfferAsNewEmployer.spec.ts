import { test, expect } from '@playwright/test';
import { studyProgramMocks } from '.././Helper/Mocks/studyProgram.mock';
import { employerMocks } from '.././Helper/Mocks/employer.mock';
import { cityMocks } from '.././Helper/Mocks/city.mock';
import { employmentScheduleMocks } from '.././Helper/Mocks/employmentSchedule.mock';
import { jobOfferMocks } from '.././Helper/Mocks/jobOffer.mock';

test.describe('createNewJobOffer', () => {

  test.beforeEach(async ({ page }) => {
    await page.route(studyProgramMocks.success.url, async route => {
      const status = studyProgramMocks.success.response.status;
      const json = studyProgramMocks.success.response.json;

      await route.fulfill({ json, status });
    });

    await page.route(employerMocks.success.url, async route => {
      const status = employerMocks.notFound.response.status;
      const json = employerMocks.notFound.response.json;

      await route.fulfill({ json, status });
    });

    await page.route(cityMocks.success.url, async route => {
      const status = cityMocks.success.response.status;
      const json = cityMocks.success.response.json;

      await route.fulfill({ json, status });
    });

    await page.route(employmentScheduleMocks.success.url, async route => {
      const status = employmentScheduleMocks.success.response.status;
      const json = employmentScheduleMocks.success.response.json;

      await route.fulfill({ json, status });
    });

    await page.route(jobOfferMocks.jobOfferNew.url, async route => {
      const status = jobOfferMocks.jobOfferNew.response.status;
      const json = jobOfferMocks.jobOfferNew.response.json;
      await route.fulfill({ json, status });
    })

    await page.route(jobOfferMocks.jobOfferEmployer.url, async route => {
      const status = jobOfferMocks.jobOfferEmployer.response.status;
      const json = jobOfferMocks.jobOfferEmployer.response.json;
      await route.fulfill({ json, status });
    })

    await page.route(jobOfferMocks.jobOfferVerifyURL.url, async route => {
      const status = jobOfferMocks.jobOfferVerifyURL.response.status;
      const json = jobOfferMocks.jobOfferVerifyURL.response.json;
      await route.fulfill({ json, status });
    })

    // se connecte au site (ADDRESSE A CHANGER LORSQUE LE SITE SERA DÉPLOYÉ)
    await page.goto('http://localhost:5002/dashboard');
    await page.waitForLoadState('networkidle');
    if (await page.locator("#cookieBannerOk")) {
      await page.locator("#cookieBannerOk").click()
    }
  });

  test('nouvelle offre', async ({ page }) => {

    await page.getByRole('button', { name: 'Créer une nouvelle offre' }).click();
    await page.locator('#titre').first().click();
    await page.locator('#titre').first().fill('Offre 1');
    await page.locator('#address').first().click();
    await page.locator('#address').first().fill('Addresse 1');
    await page.locator('#email').first().click();
    await page.locator('#email').first().fill('email@email.com');
    await page.locator('#phone').click();
    await page.locator('#phone').fill('4188886666');
    await page.getByPlaceholder('Choisir ville...').click();
    await page.getByRole('option', { name: 'Abercorn' }).click();
    await page.locator('#titre').nth(1).click();
    await page.locator('#titre').nth(1).fill('Poste');
    await page.getByPlaceholder('Choisir période(s)').click();
    await page.getByRole('option', { name: 'temps plein' }).click();
    await page.locator('#address').nth(1).click();
    await page.locator('#address').nth(1).fill('Addresse Lieu 123');
    await page.getByLabel('Date limite pour postuler*').fill('2025-05-13');
    await page.getByPlaceholder('Choisir programme(s)').click();
    await page.getByRole('option', { name: 'Arts visuels' }).click();
    await page.getByLabel('Salaire Horaire').click();
    await page.getByLabel('Salaire Horaire').fill('44');
    await page.getByLabel('Heures/semaine*').click();
    await page.getByLabel('Heures/semaine*').fill('33');
    await page.getByLabel('Lien vers l\'offre d\'emploi détaillée').click();
    await page.getByLabel('Lien vers l\'offre d\'emploi détaillée').fill('https://google.ca');
    await page.locator('#email').nth(1).click();
    await page.locator('#email').nth(1).fill('email@email.com');
    await page.getByLabel('Description du poste*').click();
    await page.getByLabel('Description du poste*').fill('aa');
    await page.getByLabel('J\'accepte les conditions*').check();
    await page.getByRole('button', { name: 'Envoyer' }).click();
    await expect(page.locator('.modal')).toHaveCount(0);
  });

  test('Offre Invalide', async ({ page }) => {
    // valide que les messages d'erreurs existe dans le formulaire...
    // en cliquant sur le message d'erreurs et recupere le message d'erreurs
    await page.goto('http://localhost:5002/dashboard');
    await page.waitForLoadState('networkidle');
    await page.getByRole('button', { name: 'Créer une nouvelle offre' }).click();
    await page.getByRole('button', { name: 'Envoyer' }).click();

    await expect(page.getByText('Vous devez nommer votre entreprise')).toBeVisible();
    await expect(page.getByText('Vous devez ajouter une adresse à votre entreprise')).toBeVisible();
    await expect(page.getByText('Votre entreprise doit avoir un courriel')).toBeVisible();
    await expect(page.getByText('Vous devez mettre un numéro de téléphone à votre entreprise')).toBeVisible();
    await expect(page.getByText('Vous devez mettre une ville à votre entreprise')).toBeVisible();

    await page.locator('#titre').first().click();
    await page.locator('#titre').first().fill('Test entreprise');

    await page.locator('#address').first().click();
    await page.locator('#address').first().fill('123');

    await page.locator('#email').first().click();
    await page.locator('#email').first().fill('test@gmail.com');

    await page.locator('#phone').click();
    await page.locator('#phone').fill('123333');

    await page.getByPlaceholder('Choisir ville...').click();
    await page.getByRole('option', { name: 'Abercorn' }).click();
    await page.getByRole('button', { name: 'Envoyer' }).click();

    await expect(page.getByText('Vous devez nommer votre entreprise')).toBeHidden();
    await expect(page.getByText('Vous devez ajouter une adresse à votre entreprise')).toBeHidden();
    await expect(page.getByText('Votre entreprise doit avoir un courriel')).toBeHidden();
    await expect(page.getByText('Vous devez mettre un numéro de téléphone à votre entreprise')).toBeHidden();
    await expect(page.getByText('Vous devez mettre une ville à votre entreprise')).toBeHidden();

    await expect(page.getByText('Le titre du poste est requis')).toBeVisible()
    await expect(page.getByText('Le type d\'emploi est requis')).toBeVisible()
    await expect(page.getByText('L\'adresse du lieu de travail est requise')).toBeVisible()
    await expect(page.getByText('Le programme visé est requis')).toBeVisible()
    await expect(page.getByText('Le salaire est requis')).toBeVisible()
    await expect(page.getByText('Veuillez entrer un nombre d\'heure valide !')).toBeVisible()
    await expect(page.getByText('Le courriel est requis')).toBeVisible()
    await expect(page.getByText('La description de l\'offre est requise')).toBeVisible()
    await expect(page.getByText('Vous devez accepter les conditions')).toBeVisible()

    await page.locator('#titre').nth(1).click();
    await page.locator('#titre').nth(1).fill('Test poste');

    await page.getByPlaceholder('Choisir période(s)').click();
    await page.getByRole('option', { name: 'temps plein' }).click();

    await page.locator('#address').nth(1).click();
    await page.locator('#address').nth(1).fill('Addresse 123');

    await page.getByPlaceholder('Choisir programme(s)').click();
    await page.getByRole('option', { name: 'Arts visuels' }).click();

    await page.getByLabel('Salaire Horaire').click();
    await page.getByLabel('Salaire Horaire').fill('32');

    await page.getByLabel('Heures/semaine*').click();
    await page.getByLabel('Heures/semaine*').fill('40');

    await page.getByLabel('Lien vers l\'offre d\'emploi détaillée').click();
    await page.getByLabel('Lien vers l\'offre d\'emploi détaillée').fill('https://google.ca');

    await page.locator('#email').nth(1).click();
    await page.locator('#email').nth(1).fill('test@gmail.com');

    await page.getByLabel('Description du poste*').click();
    await page.getByLabel('Description du poste*').fill('Test description');

    await page.getByRole('button', { name: 'Envoyer' }).click();

    await expect(page.getByText('Le courriel est requis')).toBeHidden()
    await expect(page.getByText('La description de l\'offre est requise')).toBeHidden()
    await expect(page.getByText('Veuillez entrer un nombre d\'heure valide !')).toBeHidden()
    await expect(page.getByText('Le salaire est requis')).toBeHidden()
    await expect(page.getByText('Le programme visé est requis')).toBeHidden()
    await expect(page.getByText('L\'adresse du lieu de travail')).toBeHidden()
    await expect(page.getByText('Le type d\'emploi est requis')).toBeHidden()
    await expect(page.getByText('Le titre du poste est requis')).toBeHidden()

    await page.getByLabel('J\'accepte les conditions*').check();
    await page.getByRole('button', { name: 'Envoyer' }).click();
    await expect(page.locator('.modal')).toHaveCount(0);
  });
})