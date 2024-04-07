import { test, expect } from '@playwright/test';


test.beforeEach(async ({ page }) => {
  // se connecte au site (ADDRESSE A CHANGER LORSQUE LE SITE SERA DÉPLOYÉ)
  await page.goto('http://134.122.45.61:5173/');
  await 1000;
  await page.waitForLoadState('networkidle');
});


test('Register', async ({ page }) => {
  // Ouvre la page de connexion
  // Hover sur le bouton "Offrir un emploi" pour faire apparaitre le sous-menu
  await page.hover('text=Offrir un emploi');
  // Clique sur le lien "Créer un compte entreprise"
  await page.getByRole('link', { name: 'Créer un compte entreprise' }).click();
  // Rempli les champs
  await page.getByLabel('Prénom').click();
  await page.getByLabel('Prénom').fill('Test');
  await page.getByLabel('Prénom').press('Tab');
  await page.getByLabel('Nom de famille').fill('test');
  await page.getByLabel('Nom de famille').press('Tab');
  await page.getByLabel('Nom Entreprise').fill('Test Rdl');
  await page.getByLabel('Nom Entreprise').press('Tab');
  await page.getByLabel('Adresse').fill('Route du Test');
  await page.getByLabel('Adresse').press('Tab');
  await page.getByLabel('Ville').fill('Riviere-du-Loup');
  await page.getByLabel('Ville').press('Tab');
  await page.getByLabel('Code Postal').fill('G5R1R1');
  await page.getByLabel('Code Postal').press('Tab');
  await page.getByLabel('Province').click();
  await page.getByLabel('Province').fill('Quebec');
  await page.getByLabel('Province').press('Tab');
  await page.getByLabel('Courriel').fill('test');
  await page.getByLabel('Courriel').press('Alt+Control+2');
  await page.getByLabel('Courriel').fill('test@test.ca');
  await page.getByLabel('Mot de passe').click();
  await page.getByLabel('Mot de passe').fill('Patate123');
  await page.locator('#confirm_password').click();
  await page.locator('#confirm_password').fill('Patate123');
  //confirme la création du compte
  await page.getByRole('button', { name: 'Créer' }).click();

  // MANQUE LA VALIDATION AVEC API... A faire
});

test('Login', async ({ page }) => {
  // Ouvre la page de connexion
  // Hover sur le bouton "Offrir un emploi" pour faire apparaitre le sous-menu
  await page.hover('text=Offrir un emploi');
  await page.getByRole('link', { name: 'Connexion Entreprise' }).click();
  await page.getByLabel('Nom d\'utilisateur').click();
  await page.getByLabel('Nom d\'utilisateur').fill('test@test.ca');
  await page.getByLabel('Nom d\'utilisateur').press('Tab');
  await page.getByLabel('Mot de passe').fill('Patate123');
  // Clique sur le bouton de connexion
  await page.getByRole('button', { name: 'Se connecter' }).click();
  // MANQUE LA VALIDATION AVEC API... A faire
});

test('Mauvais Login', async ({ page }) => {
  // Ouvre la page de connexion
  // Hover sur le bouton "Offrir un emploi" pour faire apparaitre le sous-menu
  await page.hover('text=Offrir un emploi');
  await page.getByRole('link', { name: 'Connexion Entreprise' }).click();
  await page.getByLabel('Nom d\'utilisateur').click();
  await page.getByLabel('Nom d\'utilisateur').fill('test');
  await page.getByRole('button', { name: 'Se connecter' }).click();

  await page.getByText('Le mot de passe est requis').click();

  // Clique sur le bouton de connexion
  await page.getByRole('button', { name: 'Se connecter' }).click();
  await page.getByText('Le courriel n\'est pas valide').click();
  // Mettre des valeurs valides
  await page.getByLabel('Nom d\'utilisateur').click();
  await page.getByLabel('Nom d\'utilisateur').fill('test@cegeprdl.ca');
  await page.getByLabel('Mot de passe').fill('Patate123');

  await page.getByRole('button', { name: 'Se connecter' }).click();

});

test('Forgot Password', async ({ page }) => {
  // Ouvre la page de connexion
  // Hover sur le bouton "Offrir un emploi" pour faire apparaitre le sous-menu
  await page.hover('text=Offrir un emploi');
  // Clique sur le lien "Connexion Entreprise"
  await page.getByRole('link', { name: 'Connexion Entreprise' }).click();
  // Clique sur le lien "Mot de passe oublié ?"
  await page.getByRole('link', { name: 'Mot de passe oublié ?' }).click();
  await page.getByLabel('Entrez votre courriel').click();
  await page.getByLabel('Entrez votre courriel').fill('test@test.ca');
  await page.getByRole('button', { name: 'Confirmer' }).click();
  // MANQUE LA VALIDATION AVEC API... A faire
});

test('Mauvais register', async ({ page }) => {
  const courrielTest = 'courrielInvalide';

   // Ouvre la page de connexion
  // Hover sur le bouton "Offrir un emploi" pour faire apparaitre le sous-menu
  await page.hover('text=Offrir un emploi');
  // Clique sur le lien "Créer un compte entreprise"
  await page.getByRole('link', { name: 'Créer un compte entreprise' }).click();
  // Soumet le formulaire sans remplir les champs
  await page.getByRole('button', { name: 'Créer' }).click();

  // FIRST NAME ############################################################################################################
  // Vérifie que le message d'erreur est correct
  await page.getByText('Prénom requis').click();
  await page.getByLabel('Prénom').click();
  await page.getByLabel('Prénom').fill('Test2');
  // ########################################################################################################################


  // LAST NAME ############################################################################################################
  await page.getByRole('button', { name: 'Créer' }).click();

  // Vérifie que le message d'erreur est correct
  await page.getByText('Nom de famille requis').click();
  await page.getByLabel('Nom de famille').click();
  await page.getByLabel('Nom de famille').fill('test2');
  // ########################################################################################################################

  // LAST NAME ############################################################################################################
  await page.getByRole('button', { name: 'Créer' }).click();
  // Vérifie que le message d'erreur est correct
  await page.getByText("Nom de l'entreprise requis").click();
  await page.getByLabel('Nom Entreprise').click();
  await page.getByLabel('Nom Entreprise').fill('Test Enteprise');
  // ########################################################################################################################

  // ADRESSE ############################################################################################################
  await page.getByRole('button', { name: 'Créer' }).click();
  // Vérifie que le message d'erreur est correct
  await page.getByText('Adresse requise').click();
  await page.getByLabel('Adresse').click();
  await page.getByLabel('Adresse').fill('Test Enteprise');
  // ########################################################################################################################

  // ADRESSE ############################################################################################################
  await page.getByRole('button', { name: 'Créer' }).click();
  // Vérifie que le message d'erreur est correct
  await page.getByText('Ville requise').click();
  await page.getByLabel('Ville').click();
  await page.getByLabel('Ville').fill('Test Riviere du Loup');
  // ########################################################################################################################

  // CODEPOSTAL ############################################################################################################
  await page.getByRole('button', { name: 'Créer' }).click();
  // Vérifie que le message d'erreur est correct
  await page.getByText('Code postal requis').click();
  await page.getByLabel('Code Postal').click();
  await page.getByLabel('Code Postal').fill('G1G 1G1');
  // ########################################################################################################################


  // PROVINCE ############################################################################################################
  await page.getByRole('button', { name: 'Créer' }).click();
  // Vérifie que le message d'erreur est correct
  await page.getByText('Province requise').click();
  await page.getByLabel('Province').click();
  await page.getByLabel('Province').fill('Quebec');
  // ########################################################################################################################


  // COURRIEL ############################################################################################################
  await page.getByRole('button', { name: 'Créer' }).click();
  // Vérifie que le message d'erreur est correct
  await page.getByText('Courriel requis').click();
  await page.getByLabel('Courriel').click();
  await page.getByLabel('Courriel').fill('courrielInvalide');
  // COURRIEL VALIDE  -------------------------------------------------------------------------------------------------------------------------

  await page.getByLabel('Courriel').click();
  await page.getByLabel('Courriel').fill('test@cegeprdl.ca');

  // ########################################################################################################################

  // MOT DE PASSE ############################################################################################################
  await page.getByRole('button', { name: 'Créer' }).click();

  // Vérifie que le message d'erreur est correct
  await page.getByText('Ne correspond pas aux critères de sécurité').click();
  await page.getByLabel('Mot de passe').click();

  await page.getByLabel('Mot de passe').click();
  await page.getByLabel('Mot de passe').fill('P@t@t31234567!');
  await page.getByRole('button', { name: 'Créer' }).click();
  await page.getByText('Les mots de passes ne').click();
  await page.locator('#confirm_password').click();
  await page.locator('#confirm_password').fill('P@t@t31234567!');
  await page.getByRole('button', { name: 'Créer' }).click();
  // ########################################################################################################################

  // CONFIRMATION MOT DE PASSE ############################################################################################################
  await page.getByRole('button', { name: 'Créer' }).click();

  // ########################################################################################################################

  // FIN DU TEST : TOUT LES CHAMPS REQUIRED SONT VALIDE ######################################################################

});
