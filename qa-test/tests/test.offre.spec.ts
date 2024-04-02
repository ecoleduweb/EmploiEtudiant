import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
    // se connecte au site (ADDRESSE A CHANGER LORSQUE LE SITE SERA DÉPLOYÉ)
    await page.goto('http://localhost:5173/offre');
    await 1000;
    await page.waitForLoadState('networkidle');
  });


  test('Ajouter un Offre', async ({ page }) => {

    await page.goto('http://localhost:5173');
    await 1000;
    await page.waitForLoadState('networkidle');
    
await page.getByRole('button', { name: 'Offrir un emploi test' }).click();
await page.getByRole('link', { name: 'Connexion entreprise' }).click();
    
    await page.getByLabel('Nom d\'utilisateur').click();
    await page.getByLabel('Nom d\'utilisateur').fill('test@test.ca');
    await page.getByLabel('Nom d\'utilisateur').press('Tab');
    await page.getByLabel('Mot de passe').fill('phil123');
    // Clique sur le bouton de connexion
    await page.getByRole('button', { name: 'Se connecter' }).click();

    await page.getByRole('button', { name: 'Trouver un emploi test' }).click();

    await page.locator('#titre').click();
    await page.locator('#titre').fill('Test');
    await page.locator('#titre').press('Tab');
    await page.getByLabel('Type d\'emplois*').click();
    await page.getByRole('option', { name: 'Emploi d\'été' }).click();

    await page.locator('#address').click();
    await page.locator('#address').fill('Adresse Test');
    await page.getByLabel('Date d\'entrée en fonction*').fill('2025-03-21');
    await page.getByLabel('Date limite pour postuler*').fill('2025-03-19');

    await page.getByPlaceholder('Choisir programme(s)').click();
    await page.getByRole('option', { name: 'Informatique' }).click();
    await page.getByRole('option', { name: 'Éducation à l\'enfance' }).click();
    await page.getByRole('option', { name: 'Inhalothérapie' }).click();
    await page.getByLabel('Heure/Semaine*').click();
    await page.getByLabel('Heure/Semaine*').fill('25');
    await page.getByLabel('Salaire/H (0.00)').click();
    await page.getByLabel('Salaire/H (0.00)').fill('21');
    await page.getByLabel('Stage ?').check();
    await page.locator('#compliantEmployer').check();
    await page.getByLabel('Urgente').check();
    await page.getByLabel('Lien*').click();
    await page.getByLabel('Lien*').fill('http://www.test.ca');
    await page.locator('#email').click();
    await page.locator('#email').fill('Test@test.ca');
    await page.getByLabel('Description du poste*').click();
    await page.getByLabel('Description du poste*').fill('Test Description');
    await page.getByRole('button', { name: 'Enregistrer' }).click();
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
await page.getByLabel('Stage ?').check();
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