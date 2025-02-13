# Description

Liste à cocher pour t'aider à faire une revue de code efficace.

## Qualité du code

- [ ] Les noms des variables, fonctions et classes sont descriptifs et suivent les conventions de nommage du projet. Ex: `calculateTotalPrice()` vs `calc()` ou `userFirstName` vs `ufn`.
- [ ] Le code ne se répète pas pour rien (copier collé au lien de tout centraliser dans une méthode)
- [ ] Le code respecte l'architecture actuelle

## Tests

- [ ] Les tests sont ajoutés ou modifiés
- [ ] Les tests testent les cas valides
- [ ] Les tests testent tous les cas fautifs

## Documentation

- [ ] La documentation a été mise à jour si nécessaire

## Gestion des erreurs

- [ ] On affiche toujours un message d'erreur en cas de problème (pas de catch vide ou de return; en cas d'erreur)
- [ ] On utilise le logger pour logger les erreurs
