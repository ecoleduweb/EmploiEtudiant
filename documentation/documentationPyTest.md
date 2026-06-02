# Guide d'installation et de test Pytest

## Installation de l'environnement

```bash
# Création d'un environnement virtuel nommé venv
python -m venv venv

# Activation de l'environnement virtuel
venv\Scripts\activate

# Mise à jour de pip
pip install --upgrade pip

# Installation des dépendances
pip install flask pytest pytest-flask sqlalchemy flask-sqlalchemy python-argon2
```

## Dépendances du projet

- **flask**: Framework web pour l'application
- **pytest**: Framework de test
- **pytest-flask**: Support pour tester Flask
- **sqlalchemy**: ORM pour la base de données
- **flask-sqlalchemy**: Intégration SQLAlchemy avec Flask
- **python-argon2**: Pour le hachage des mots de passe avec Argon2

## Structure des tests

### Étape 1: Préparation avec les Fixtures

```python
# Fixture app
@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        # Ajout des données de test: entreprises, employeurs, offres d'emploi, utilisateurs...
        yield app
        db.session.remove()
        db.drop_all()

# Fixture client
@pytest.fixture(scope='module')
def client(app):
    return app.test_client()
```

#### Rôle des fixtures:
- **Fixture app**: Crée une instance Flask avec une base SQLite en mémoire, initialise les tables, insère des données de test (2 offres, 2 utilisateurs, etc.), et nettoie après les tests
- **Fixture client**: Fournit un client de test Flask pour envoyer des requêtes HTTP (GET, POST, PUT, DELETE) aux endpoints
- En bref , ce sont les données qui seront utilisées pour vos test , elles sont dans une base de donnée SQLite (volatile) 

### Exemple de test: Suppression d'une offre d'emploi

```python
def test_deleteJobOfferAsAdmin(client):
    # Authentification de l'admin
    data1 = {"email": "admin@gmail.com", "password": "test123"}
    response1 = client.post('/auth/login', json=data1)
    token = response1.json['token']
    
    # Requête de suppression
    response2 = client.delete(f'/jobOffer/1', headers={'Authorization': token})
    
    # Vérifications
    assert response2.status_code == 200
    assert response2.json['message'] == 'Job offer deleted'
```

#### Objectif du test:
1. Authentifier l'admin (admin@gmail.com)
2. Envoyer une requête DELETE à /jobOffer/1
3. Vérifier que le statut est 200 et que le message confirme la suppression

## Lancement des tests

Pour exécuter les tests:

```bash
pytest
```