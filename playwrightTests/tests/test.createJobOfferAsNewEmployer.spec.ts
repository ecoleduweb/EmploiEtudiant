import { test, expect } from '@playwright/test';
test.describe('createNewJobOffer', () => {

  test.beforeEach(async ({ page }) => {
    // se connecte au site (ADDRESSE A CHANGER LORSQUE LE SITE SERA DÉPLOYÉ)
    await page.goto('http://localhost:5002');
    await page.waitForLoadState('networkidle');
    if (await page.locator("#cookieBannerOk")) {
      await page.locator("#cookieBannerOk").click()
    }

    await page.locator('#loginDropDown').hover();
    await page.getByRole('link', { name: 'Connexion entreprise' }).click();
    await page.getByLabel('Nom d\'utilisateur').click();
    await page.getByLabel('Nom d\'utilisateur').fill('admin@gmail.com');
    await page.getByLabel('Mot de passe').click();
    await page.getByLabel('Mot de passe').fill('test123');
    await page.getByRole('button', { name: 'Se connecter' }).click();
    await page.goto('http://localhost:5002/programmes');
    await page.waitForLoadState('networkidle');

    await page.getByRole('button', { name: 'Créer un nouveau programme' }).click();
    await page.getByPlaceholder('Nouveau nom').click();
    await page.getByPlaceholder('Nouveau nom').fill('Programme 1');
    await page.getByRole('button', { name: 'Créer', exact: true }).click();

    await page.getByRole('button', { name: 'Créer un nouveau programme' }).click();
    await page.getByPlaceholder('Nouveau nom').click();
    await page.getByPlaceholder('Nouveau nom').fill('Programme 2');
    await page.getByRole('button', { name: 'Créer', exact: true }).click();

    await page.getByRole('button', { name: 'Déconnexion Logout icon' }).click();

    await page.goto('http://localhost:5002');
    await page.waitForLoadState('networkidle');
    await page.locator('#loginDropDown').hover();

    await page.getByRole('link', { name: 'Créer un compte entreprise' }).click();
    await page.getByLabel('Prénom').click();
    await page.getByLabel('Prénom').fill('test');
    await page.getByLabel('Nom de famille').click();
    await page.getByLabel('Nom de famille').fill('test');
    await page.locator('div').filter({ hasText: 'Courriel' }).nth(4).click();
    const uniqueEmail = `${new Date().getTime()}@gmail.com`
    await page.getByLabel('Courriel').fill(uniqueEmail);
    await page.getByLabel('Courriel').press('Tab');
    await page.getByLabel('Mot de passe').fill('AAAaaa111!!!');
    await page.locator('div').filter({ hasText: 'Valider Mot de passe' }).nth(4).click();
    await page.locator('#confirm_password').fill('AAAaaa111!!!');
    await page.getByRole('button', { name: 'Créer' }).click();
  });

  test.only('nouvelle offre', async ({ page }) => {
    await page.goto('http://localhost:5002');

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
    await page.getByRole('option', { name: 'ville' }).click();
    await page.locator('#titre').nth(1).click();
    await page.locator('#titre').nth(1).fill('Poste');
    await page.getByPlaceholder('Choisir période(s)').click();
    await page.getByRole('option', { name: 'temps plein' }).click();
    await page.locator('#address').nth(1).click();
    await page.locator('#address').nth(1).fill('Addresse Lieu 123');
    await page.getByLabel('Date limite pour postuler*').fill('2024-08-04');
    await page.getByPlaceholder('Choisir programme(s)').click();
    await page.getByRole('option', { name: 'Programme 1' }).click();
    await page.getByLabel('Salaires Horaire').click();
    await page.getByLabel('Salaires Horaire').fill('44');
    await page.getByLabel('Heures/semaine*').click();
    await page.getByLabel('Heures/semaine*').fill('33');
    await page.locator('#email').nth(1).click();
    await page.locator('#email').nth(1).fill('email@email.com');
    await page.getByLabel('Description du poste*').click();
    await page.getByLabel('Description du poste*').fill('aa');
    await page.getByLabel('J\'acceptes les condtions').check();
    await page.getByRole('button', { name: 'Envoyer' }).click();

    await page.getByRole('button', { name: 'modifier' }).click();
    await page.locator('#titre').nth(1).click();
    await page.locator('#titre').nth(1).fill('Poste modifier');
    await page.getByLabel('Date limite pour postuler*').fill('2024-09-08');
    await page.locator('#programme').click();
    await page.getByRole('option', { name: 'Programme 2' }).click();
    await page.getByLabel('J\'acceptes les condtions').check();
    await page.getByRole('button', { name: 'Envoyer' }).click();
  });

  test('Offre Invalide', async ({ page }) => {
    // valide que les messages d'erreurs existe dans le formulaire...
    // en cliquant sur le message d'erreurs et recupere le message d'erreurs
    await page.goto('http://localhost:5002/dashboard');
    await page.waitForLoadState('networkidle');

    await page.getByRole('button', { name: 'Créer une nouvelle offre' }).click();
    await page.getByRole('button', { name: 'Envoyer' }).click();

    await expect(page.getByText('Vous devez nommer votre')).toBeVisible();
    await expect(page.getByText('Vous devez ajouter une')).toBeVisible();
    await expect(page.getByText('Vous devez mettre un courriel à')).toBeVisible();
    await expect(page.getByText('Vous devez mettre un numéro')).toBeVisible();
    await expect(page.getByText('Vous devez mettre une ville')).toBeVisible();

    await page.locator('#titre').first().click();
    await page.locator('#titre').first().fill('Test entreprise');
    await page.getByRole('button', { name: 'Envoyer' }).click();
    await expect(page.getByText('Vous devez nommer votre')).toBeHidden();

    await page.locator('#address').first().click();
    await page.locator('#address').first().fill('123');
    await page.getByRole('button', { name: 'Envoyer' }).click();
    await expect(page.getByText('Vous devez ajouter une')).toBeHidden();

    await page.locator('#email').first().click();
    await page.locator('#email').first().fill('test@gmail.com');
    await page.getByRole('button', { name: 'Envoyer' }).click();
    await expect(page.getByText('Vous devez mettre un courriel à')).toBeHidden();

    await page.locator('#phone').click();
    await page.locator('#phone').fill('123333');
    await page.getByRole('button', { name: 'Envoyer' }).click();
    await expect(page.getByText('Vous devez mettre un numéro')).toBeHidden();

    await page.getByPlaceholder('Choisir ville...').click();
    await page.getByRole('option', { name: 'ville' }).click();
    await page.getByRole('button', { name: 'Envoyer' }).click();
    await expect(page.getByText('Vous devez mettre une ville')).toBeHidden();

    await expect(page.getByText('Le titre du poste est requis')).toBeVisible()
    await expect(page.getByText('Le type d\'emplois est requis')).toBeVisible()
    await expect(page.getByText('L\'adresse du lieu de travail')).toBeVisible()
    await expect(page.getByText('Le programme visé est requis')).toBeVisible()
    await expect(page.getByText('Le salaire est requis')).toBeVisible()
    await expect(page.getByText('Veuillez entrer un nombre d\'')).toBeVisible()
    await expect(page.getByText('Le courriel est requis')).toBeVisible()
    await expect(page.getByText('La description de l\'offre est')).toBeVisible()
    await expect(page.getByText('Vous devez accepter les')).toBeVisible()

    await page.locator('#titre').nth(1).click();
    await page.locator('#titre').nth(1).fill('Test poste');
    await page.getByRole('button', { name: 'Envoyer' }).click();
    await expect(page.getByText('Le titre du poste est requis')).toBeHidden()

    await page.getByPlaceholder('Choisir période(s)').click();
    await page.getByRole('option', { name: 'temps plein' }).click();
    await page.getByRole('button', { name: 'Envoyer' }).click();
    await expect(page.getByText('Le type d\'emplois est requis')).toBeHidden()

    await page.locator('#address').nth(1).click();
    await page.locator('#address').nth(1).fill('Addresse 123');
    await page.getByRole('button', { name: 'Envoyer' }).click();
    await expect(page.getByText('L\'adresse du lieu de travail')).toBeHidden()

    await page.getByPlaceholder('Choisir programme(s)').click();
    await page.getByRole('option', { name: 'Programme 1' }).click();
    await page.getByRole('button', { name: 'Envoyer' }).click();
    await expect(page.getByText('Le programme visé est requis')).toBeHidden()

    await page.getByLabel('Salaires Horaire').click();
    await page.getByLabel('Salaires Horaire').fill('32');
    await page.getByRole('button', { name: 'Envoyer' }).click();
    await expect(page.getByText('Le salaire est requis')).toBeHidden()

    await page.getByLabel('Heures/semaine*').click();
    await page.getByLabel('Heures/semaine*').fill('40');
    await page.getByRole('button', { name: 'Envoyer' }).click();
    await expect(page.getByText('Veuillez entrer un nombre d\'')).toBeHidden()

    await page.locator('#email').nth(1).click();
    await page.locator('#email').nth(1).fill('test@gmail.com');
    await page.getByRole('button', { name: 'Envoyer' }).click();
    await expect(page.getByText('Le courriel est requis')).toBeHidden()

    await page.getByLabel('Description du poste*').click();
    await page.getByLabel('Description du poste*').fill('Test description');
    await page.getByRole('button', { name: 'Envoyer' }).click();
    await expect(page.getByText('La description de l\'offre est')).toBeHidden()

    await page.getByLabel('J\'acceptes les condtions').check();
    await page.getByRole('button', { name: 'Envoyer' }).click();

    await expect(await page.getByText('Test poste')).toBeVisible()

    await page.getByRole('button', { name: 'modifier' }).click();
    await page.waitForLoadState('networkidle');

    await expect(page.getByText('Nom* Test entreprise')).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Mon entreprise' })).toBeVisible();
  });
})