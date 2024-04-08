import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  
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
await page.getByLabel('Salaire/H*').click();
await page.getByLabel('Salaire/H*').fill('21');
await page.getByLabel('Stage ?').check();
await page.locator('#compliantEmployer').check();
await page.getByLabel('Urgente').check();
await page.getByLabel('Lien*').click();
await page.getByLabel('Lien*').fill('test.ca');
await page.locator('#email').click();
await page.locator('#email').fill('Test Contact');
await page.getByLabel('Description du poste*').click();
await page.getByLabel('Description du poste*').fill('Test Description');
await page.getByRole('button', { name: 'Enregistrer' }).click();
});
