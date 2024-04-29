import pytest
from app import create_app, db
from argon2 import PasswordHasher
hasher=PasswordHasher()
from app.models.user_model import User

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
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

def test_linkOfferProgram(client):
    dataLogin = {
        "email": "test@test.com",
        "password": "test",
    }
    responseLogin = client.post('/user/login', json=dataLogin)
    token = responseLogin.json['token']
    data = {
        "studyProgramId": 1,
        "offerId": 1
    }
    response = client.post('/offerProgram/linkOfferProgram', json=data, headers={"Authorization": token})
    assert response.status_code == 200

