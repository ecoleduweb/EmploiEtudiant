import pytest
from app import create_app, db
from app.models.employers_model import Employers
from app.models.enterprise_model import Enterprise
from app.models.user_model import User
from argon2 import PasswordHasher

hasher = PasswordHasher()


@pytest.fixture(scope="module")
def app():
    app = create_app()

    with app.app_context():
        db.create_all()

        e1 = Enterprise(
            id=1,
            name="Développeur",
            email="test@test.com",
            phone="123-123-1234",
            address="123 rue de la",
            isTemporary=False,
            cityId=1,
        )
        e2 = Enterprise(
            id=2,
            name="Développeur",
            email="test2@test.com",
            phone="123-123-1234",
            address="123 rue de la",
            isTemporary=True,
            cityId=1,
        )
        db.session.add_all([e1, e2])

        user = User(
            id=1,
            firstName="test",
            lastName="test",
            email="test@test.com",
            password=hasher.hash("test"),
            isModerator=True,
            active=True,
        )
        db.session.add(user)

        employer = Employers(
            id=1,
            verified=True,
            userId=1,
            enterpriseId=1,
        )
        db.session.add(employer)

        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def client(app):
    with app.test_client() as client:
        res = client.post(
            "/user/login",
            json={"email": "test@test.com", "password": "test"},
        )
        assert res.status_code == 200
        yield client


def test_getEnterprises(client):
    response = client.get("/enterprise/all")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 2


def test_createEnterprise(client):
    payload = {
        "name": "Nouvelle entreprise",
        "email": "new@test.com",
        "phone": "555-555-5555",
        "address": "456 rue test",
        "cityId": 1,
        "userIds": []
    }

    response = client.post("/enterprise/new", json=payload)
    assert response.status_code == 200

    data = response.json
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["phone"] == payload["phone"]
    assert data["address"] == payload["address"]
    assert data["cityId"] == 1
    assert data["isTemporary"] is False
    assert "id" in data


def test_getEnterprise(client):
    response = client.get("/enterprise/1")
    assert response.status_code == 200

    data = response.json
    assert data["id"] == 1
    assert "users" in data
    assert isinstance(data["users"], list)


def test_checkIfUserHaveEnterprise(client):
    response = client.get("/enterprise/currentEnterprise")
    assert response.status_code == 200

    data = response.json
    assert data["id"] == 1
    assert "users" in data


def test_updateEnterprise(client):
    payload = {
        "name": "Entreprise modifiée",
        "email": "mod@test.com",
        "phone": "999-999-9999",
        "address": "Rue modifiée",
        "cityId": 1,
        "userIds": []
    }

    response = client.put("/enterprise/1", json=payload)
    assert response.status_code == 200
    assert response.json["message"] == "enterprise updated"


def test_checkIfUserHaveEnterprise_new_user(client):
    response = client.post(
        "/user/register",
        json={
            "firstName": "Nouvel",
            "lastName": "Utilisateur",
            "email": "newuser@test.com",
            "password": "test123",
            "role": "user",
            "captchaToken": "fake",
        },
    )
    assert response.status_code == 200

    res = client.post(
        "/user/login",
        json={"email": "newuser@test.com", "password": "test123"},
    )
    assert res.status_code == 200

    response = client.get("/enterprise/currentEnterprise")
    assert response.status_code == 404
