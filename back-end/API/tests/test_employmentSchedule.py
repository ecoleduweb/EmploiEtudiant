import pytest
from app import create_app, db
from app.models.employmentSchedule_model import EmploymentSchedule
from app.models.user_model import User
from argon2 import PasswordHasher

hasher = PasswordHasher()


@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        data1 = {
            "id": 1,
            "description": "Temps plein"
        }
        employmentSchedule1 = EmploymentSchedule(**data1)
        db.session.add(employmentSchedule1)
        data2 = {
            "id": 2,
            "description": "Temps partiel"
        }
        employmentSchedule2 = EmploymentSchedule(**data2)
        db.session.add(employmentSchedule2)
        hashed_password = hasher.hash("test123")
        user = User(id=1, firstName="Robert", lastName="Lizotte", email="test@gmail.com", password=hashed_password, active=True, isModerator=False)
        db.session.add(user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

def test_employmentSchedules(client):
    dataLogin = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    responseLogin = client.post('/user/login', json=dataLogin)
    token = responseLogin.json['token']
    response = client.get('/employmentSchedule/all', headers={"Authorization": token})
    assert response.status_code == 200
    assert len(response.json) == 2

def test_employmentSchedule(client):
    dataLogin = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    responseLogin = client.post('/user/login', json=dataLogin)
    token = responseLogin.json['token']
    response = client.get('/employmentSchedule/1', headers={"Authorization": token})
    assert response.status_code == 200