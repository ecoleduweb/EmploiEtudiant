import pytest
from app import create_app, db
from app.models.employers_model import Employers
from app.models.user_model import User
from app.models.enterprise_model import Enterprise

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
        db.session.add(employers)
        data = {
            "id": 1,
            "email": "test@test.com",
            "password": "test",
            "isModerator": False,
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
    return app.test_client()

def test_createEmployer(client):
    data = {
        "enterpriseId": 1,
        "userId": 1,
    }
    response = client.post('/employer/createEmployer', json=data)
    assert response.status_code == 200


def test_updateEmployer(client):
    data = {
        "verified": True,
        "userId": 1,
        "enterpriseId": 1,
    }
    response = client.put('/employer/updateEmployer/1', json=data)
    assert response.status_code == 200
    assert response.json == {
        "message": "employer updated"
    }

def test_deleteEmployer(client):
    response = client.delete('/employer/deleteEmployer/1')
    assert response.status_code == 200
    assert response.json == {
        "message": "employer deleted"
    }
