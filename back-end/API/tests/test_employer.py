import pytest
from app import create_app, db
from app.models.employers_model import Employers
from app.models.user_model import User
from app.models.enterprise_model import Enterprise
from argon2 import PasswordHasher

hasher = PasswordHasher()

@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        data = {
            "id": 1,
            "verified": True,
            "userId": 1,
            "enterpriseId": 1,
        }
        employers = Employers(**data)
        db.session.add(employers)
        data = {
            "id": 2,
            "verified": False,
            "userId": 1,
            "enterpriseId": 1,
        }
        employers = Employers(**data)
        hashed_password = hasher.hash("test")
        db.session.add(employers)
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
        data = {
            "id": 1,
            "name": "test",
            "email": "test@test.com",
            "phone": "123-456-7890",
            "address": "123 test street",
            "isTemporary": False,
            "cityId": 1,
        }
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
        assert res.status_code == 200
        yield client

def test_createEmployer(client):
    data = {
        "enterpriseId": 1,
        "userId": 1,
    }
    response = client.post('/employer/new', json=data)
    assert response.status_code == 200


def test_updateEmployer(client):
    data = {
        "verified": True,
        "userId": 1,
        "enterpriseId": 1,
    }
    
    response = client.put('/employer/1', json=data)
    assert response.status_code == 200
    assert response.json == {
        "message": "employer updated"
    }
