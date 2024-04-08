import os
import pytest
from argon2 import PasswordHasher
from app import create_app, db
from app.models.user_model import User 

hasher = PasswordHasher()

@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        hashed_password = hasher.hash("test123")
        user = User(id=1, email="test@gmail.com", password=hashed_password, active=True, isModerator=False)  # Removed 'name' attribute
        db.session.add(user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

def test_createUser(client):
    data = {
        "id": 2,
        "email": "test2@gmail.com",
        "password": "test123"
    }
    dataLogin = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    reponseLogin = client.post('/user/login', json=dataLogin)
    token = reponseLogin.json['token']
    response = client.post('/user/createUser', json=data, headers={"Authorization": token})
    assert response.status_code == 200

def test_login(client):
    data = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    response = client.post('/user/login', json=data)
    assert response.status_code == 200
    assert 'token' in response.json
