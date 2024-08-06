import pytest
from app import create_app, db
from app.models.employers_model import Employers
from app.models.enterprise_model import Enterprise
from app.models.user_model import User
from argon2 import PasswordHasher

hasher = PasswordHasher()

@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        data = {
            "id": 1,
            "name": "Développeur",
            "email": "test@test.com",
            "phone": "123-123-1234",
            "address": "123 rue de la",
            "isTemporary": False,
            "cityId": 1,
        }
        enterprise = Enterprise(**data)
        db.session.add(enterprise)
        data = {
            "id": 2,
            "name": "Développeur",
            "email": "test2@test.com",
            "phone": "123-123-1234",
            "address": "123 rue de la",
            "isTemporary": True,
            "cityId": 1,
        }
        enterprise = Enterprise(**data)
        db.session.add(enterprise)
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
        
        data = {
            "id": 1,
            "verified": True,
            "userId": 1,
            "enterpriseId": 3,
        }
        employers = Employers(**data)
        db.session.add(employers)

        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

def test_getEnterprises(client):
    dataLogin = {
        "email": "test@test.com",
        "password": "test",
    }
    responseLogin = client.post('/user/login', json=dataLogin)
    token = responseLogin.json['token']
    response = client.get('/enterprise/all', headers={"Authorization": token})
    assert response.status_code == 200
    assert len(response.json) == 2

def test_createEnterprise(client):
    data = {
        "name": "Développeur",
        "email": "testTest@gmail.com",
        "phone": "123-123-1234",
        "address": "123 rue de la",
        "cityId": 1,
    }
    dataLogin = {
        "email": "test@test.com",
        "password": "test",
    }
    responseLogin = client.post('/user/login', json=dataLogin)
    token = responseLogin.json['token']
    response = client.post('/enterprise/new', json=data, headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json == {
        "id": 3,
        "name": "Développeur",
        "email": "testTest@gmail.com",
        "phone": "123-123-1234",
        "address": "123 rue de la",
        "isTemporary": False,
        "cityId": 1,
    }

def test_getEnterprise(client):
    dataLogin = {
        "email": "test@test.com",
        "password": "test",
    }
    responseLogin = client.post('/user/login', json=dataLogin)
    token = responseLogin.json['token']
    response = client.get('/enterprise/1', headers={"Authorization": token})
    assert response.status_code == 200
    assert len(response.json) == 7

def test_updateEnterprise(client):
    data = {
        "id": 3,
        "name": "Développeur modifié",
        "email": "test@test.com",
        "phone": "123-123-1234",
        "address": "123 rue de la",
        "cityId": 1,
    }
    dataLogin = {
        "email": "test@test.com",
        "password": "test",
    }
    responseLogin = client.post('/user/login', json=dataLogin)
    token = responseLogin.json['token']
    response = client.put('/enterprise/3', json=data, headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json == {
        "message": 'enterprise updated'
    }