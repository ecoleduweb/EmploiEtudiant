import pytest
from app import create_app, db
from app.models.enterprise_model import Enterprise


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
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

def test_getEnterprises(client):
    response = client.get('/enterprise/getEnterprises')
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
    response = client.post('/enterprise/createEnterprise', json=data)
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

def test_updateEnterprise(client):
    data = {
        "id": 1,
        "name": "Développeur modifié",
        "email": "test@test.com",
        "phone": "123-123-1234",
        "address": "123 rue de la",
        "cityId": 1,
    }
    response = client.put('/enterprise/updateEntreprise/1', json=data)
    assert response.status_code == 200
    assert response.json == {
        "message": 'enterprise updated'
    }

def test_deleteEnterprise(client):
    data = {
        "id": 2,
        "name": "Développeur",
        "email": "test2@test.com",
        "phone": "123-123-1234",
        "address": "123 rue de la",
        "cityId": 1,
    }
    response = client.delete('/enterprise/deleteEnterprise/2')
    assert response.status_code == 200
    assert response.json == {
        "message": 'enterprise deleted'
    }
