import pytest
from app import create_app, db
from argon2 import PasswordHasher
hasher=PasswordHasher()
from app.models.user_model import User
from app.models.offer_programm_model import OfferProgram

@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        hashed_password = hasher.hash("test")
        data = {
            "id": 1,
            "firstName": "test",
            "lastName": "test",
            "email": "test@test.com",
            "password": hashed_password,
            "isModerator": True,
            "active": True,
        }
        user = User(**data)
        db.session.add(user)
        db.session.add(OfferProgram(**{
            "id": 1,
            "programId": 1,
            "offerId": 1
        }))
        
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    with app.test_client() as client:
        dataLogin = {
            "email": "test@test.com",
            "password": "test",
        }
        res = client.post('/user/login', json=dataLogin)
        print(res.json)
        yield client

def test_getProgramIdByOfferId(client):
    response = client.get('/offerProgram/1')
    assert response.status_code == 200
