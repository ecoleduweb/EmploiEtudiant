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
  });

  test.only('nouvelle offre', async ({ page }) => {
    await page.goto('http://localhost:5002');
    await 1000;
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
    await page.getByLabel('Salaire/H').click();
    await page.getByLabel('Salaire/H').fill('44');
    await page.getByLabel('Heure/Semaine*').click();
    await page.getByLabel('Heure/Semaine*').fill('33');
    await page.locator('#email').nth(1).click();
    await page.locator('#email').nth(1).fill('email@email.com');
    await page.getByLabel('Description du poste*').click();
    await page.getByLabel('Description du poste*').fill('aa');
    await page.getByLabel('J\'acceptes les condtions').check();
    await page.getByRole('button', { name: 'Envoyer' }).click();

    //await page.waitForLoadState('networkidle');

    await page.getByRole('button', { name: 'modifier' }).click();
    await page.locator('#titre').nth(1).click();
    await page.locator('#titre').nth(1).fill('Poste modifier');
    await page.getByLabel('Date limite pour postuler*').fill('2024-09-08');
    await page.locator('#programme').click();
    await page.getByRole('option', { name: 'Programme 2' }).click();
    await page.getByLabel('J\'acceptes les condtions').check();
    await page.getByRole('button', { name: 'Envoyer' }).click();

    //await page.waitForLoadState('networkidle');
  });

  test('Offre Invalide', async ({ page }) => {
    // valide que les messages d'erreurs existe dans le formulaire...
    // en cliquant sur le message d'erreurs et recupere le message d'erreurs
    await page.getByRole('button', { name: 'Enregistrer' }).click();
    await page.getByText('Le titre du poste est requis').click();
    await page.locator('#titre').click();
    await page.locator('#titre').fill('Titre');

    await page.getByRole('button', { name: 'Enregistrer' }).click();
    await page.getByPlaceholder('Choisir période(s)').click();
    await page.getByRole('option', { name: 'Emploi d\'été' }).click();
    await page.getByText('Le type d\'emploi est requis').click();
    await page.getByRole('button', { name: 'Enregistrer' }).click();
    await page.locator('#address').click();
    await page.locator('#address').fill('Adresse Test');
    await page.getByText('L\'adresse du lieu de travail').click();
    await page.getByRole('button', { name: 'Enregistrer' }).click();
    await page.getByLabel('Date d\'entrée en fonction*').fill('2024-03-20');
    await page.getByText('Veuillez choisir une date').first().click();
    await page.getByRole('button', { name: 'Enregistrer' }).click();
    await page.getByLabel('Date limite pour postuler*').fill('2024-03-22');
    await page.getByText('Veuillez choisir une date').click();
    await page.getByRole('button', { name: 'Enregistrer' }).click();

    await page.getByPlaceholder('Choisir programme(s)').click();
    await page.getByRole('option', { name: 'Informatique' }).click();
    await page.locator('#programme').press('Tab');
    await page.getByText('Veuillez entrer un salaire').click();
    await page.getByRole('button', { name: 'Enregistrer' }).click();
    await page.getByLabel('Salaire/H (0.00)*').click();
    await page.getByLabel('Salaire/H (0.00)*').fill('asdd');
    await page.getByText('Veuillez entrer un salaire').click();
    await page.getByRole('button', { name: 'Enregistrer' }).click();
    await page.getByLabel('Salaire/H (0.00)*').click();
    await page.getByLabel('Salaire/H (0.00)*').fill('1.23');
    await page.getByText('Veuillez entrer un salaire').click();
    await page.getByRole('button', { name: 'Enregistrer' }).click();
    await page.getByLabel('Heure/Semaine*').click();
    await page.getByLabel('Heure/Semaine*').fill('asd');
    await page.getByRole('button', { name: 'Enregistrer' }).click();
    await page.getByLabel('Heure/Semaine*').click();
    await page.getByLabel('Heure/Semaine*').fill('23');
    await page.getByText('Veuillez entrer un nombre d\'').click();
    await page.getByRole('button', { name: 'Enregistrer' }).click();
    await page.locator('#compliantEmployer').check();
    await page.getByLabel('Urgente').check();
    await page.getByLabel('Lien*').click();
    await page.getByLabel('Lien*').fill('asd');
    await page.getByRole('button', { name: 'Enregistrer' }).click();
    await page.getByText('Le lien doit être de format').click();
    await page.getByLabel('Lien*').click();
    await page.getByLabel('Lien*').fill('https://test.ca');
    await page.getByRole('button', { name: 'Enregistrer' }).click();
    await page.locator('#email').click();

    await page.getByText('Le courriel est requis').click();
    await page.locator('#email').click();
    await page.locator('#email').fill('test');
    await page.locator('#email').press('Alt+Control+@');
    await page.getByRole('button', { name: 'Enregistrer' }).click();
    await page.getByText('Le courriel n\'est pas valide').click();
    await page.locator('#email').click();
    await page.locator('#email').press('Alt+Control+@');
    await page.locator('#email').fill('test@asdsa');
    await page.getByRole('button', { name: 'Enregistrer' }).click();
    await page.getByText('Le courriel doit être de').click();
    await page.locator('#email').click();
    await page.locator('#email').fill('test@asdsa.ca');
    await page.getByRole('button', { name: 'Enregistrer' }).click();
    await page.getByText('La description de l\'offre est').click();
    await page.getByLabel('Description du poste*').click();
    await page.getByLabel('Description du poste*').fill('Test');
    await page.getByRole('button', { name: 'Enregistrer' }).click();
  });
})