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

def test_checkIfUserHaveEnterprise(client):
    dataLogin = {
        "email": "test@test.com",
        "password": "test",
    }
    responseLogin = client.post('/user/login', json=dataLogin)
    token = responseLogin.json['token']
    response = client.get('/enterprise/currentEnterprise', headers={"Authorization": token})
    assert response.status_code == 200
    assert len(response.json) == 7

def test_checkIfUserHaveEnterprise_NewUser(client):
    data = {
        "id": 2,
        "firstName":"Test", 
        "lastName":"NouveauUser",
        "email": "test3@gmail.com",
        "password": "test123",
        "role": "user",
        "captchaToken": "03AFcWeA6bh39D5UeY9TN5C72LTE_VrIteCxQWvc0TCa2sErSF56PlrAZ3oFo5WSnaRxHnlJ3MUBm0KlhWeNs57_tq6nbFKON-DQFP3G5KyQZ5wfLb6fVKmwiyAqop77TrVOKr2B5e-mpYwyYzahOcv-AAUmFimWECWwqJqgBIIky758YeIer6XB5QsNqPeFrEDqR4bnBQiArqzguQsPu0QBs02XYtcnVc97HjUOTELPCCFtId18D6ZPvlVXYFarxffP4OkadMRZIApLd5vQOKfjj-RW9IdPCAtBDll_6k5WJiLCHQmEgkXrnEQOddTg8oaC7AeZS4q7sTTu_5QwBGi5fLbDt2i-8Xt6MQ3Jw-W97PZgAhAoywA1UmnqkhaVksnBJs4Ya_J7Hp5XY6WDSq9ngDeYCEPXXXrqWmY4H056dR8LvKzxIrtKHtjV4gEDbnGKS0m8NxmsiulMExZN-ABUI61uw8TQr8Y0Jg8mwGBnmXReg3ZVTr-LUIq-b-0rt6RTAKnY5ow2kEfAah9L0EhFcbcnM6FK1OM5ecL48bDVEWfOBMx8sSIUYsl85SogguOx8fN7ntIzVM3gCqWfcoPraPvC08rzDcaBJg9PmwMhDOkTgYDyWOwV4jrcbB_lK4quGjt_M-rynHLUIsDw49Yy4mNZuPXzAd1yxi-stlRU7ZCpYQAfw73bl4IF_stnRkEtosWUOkhlHRDJMQ7Dk9KbDn7_-cmCHnFc2I6mGBAhU2DV7RJxZE21DsOFtP6qc8N-HnMpQhEzv6Fbq_iQ6pPmB3Qm_rSvvAtPbW_AxR1wm-sqjFtNt51-sAXRYQMP70co1f2rWtb7pJL9j_FRnubjTmiGWKZX-qnMEL2RIZXuu8uONLe24F1KKz7F60_HRjC5QHEqXHKpxY7bHNp4eLsTKhFBGkrObt92K8GJfbJe5XS2sXae2rsaDtUcUu1U1DkagcM_3UgxBYQtxVzix57nge4W0_wEBJo9nQfXApBZCm9myL0ldwGuw9gQn1QnXzndlppKQa0_tUGYqnoLLwer6NzmwcxhxCLoAnLVYeXAt6xBzK3X1JsHIanjwxwZe1UNy372CRpKH1iRdqbX6jtcJyJbGRRjS7Ho28axdT-wXCEl0f2mAhL-VbXJ_Y4mwHzik8UTbJdMpLEFqr3ePT7yDFlWCBAD6VMDTlwarLHvOmqwB7t0IV_CFXeFL6YSalqvxuM3OcZftUUFRn0DMcs85eVDScWmTm89u83-6K0_NpA58vk0R2nL9ojsD5neKr1fauxnBbn5LSlxtA79RdLp0GxdCbmnxzdE_G1AibpepXCFeHgEojMWV7Qhk0Tph7WnYVGylz0LPqSNos22KrGfvf2yTmLnN-joAuuicbX4c_A6T-eqI7liTD-i_NTalgg7oumlw5C6XgPLgquJ522ueKbJLey_02GgLOhIvUAsl0WE7ZjgklQPo4QBfsybztmJbZnEuVgDZQnhPZzJH6ZE8H-snYoFoZmL3vQKZ_uVLqWrC1JJNyZgFxND2A66IhRZXp4NWTd5olcuk2ZuffRWTjJnJ_DD8G4ETCpOGocUb6YN23xOxaZS66il_Ej_U63DEopFEBgsRuJlzY_k5iX1RLuQQObUj-XO_alhCTi7KejjbJatFigDzc-gtj-t3RrHCWSwKqcOvM6FUt56NS12P5NNN2ROJ-LKh-iCdBHj8wbvm6_MPZJParB2fi3W0DbY7PPkUPmYCtqjHYcESZpbkc2l2fJNlmqYqkOUOahTAJL3kWgFvXuku0Ec5GDWhdEaT1WBQmwJGWh49f0olkGr3qI0k1oJc4c0kV_3byYaYq9y58M_9wV4oBgIFCNirJe-Es9kqRX3uE3ONicGclV8KT_0cFZveNSyIAeiIHPrtO4zU6qxXJz_J1lKRwPXFvD5QlpqilknMpQW5dJOEOgLim7WlXnbEEYd38Whj5Y_ZvuSgzTr8y75s2_XVI7FPStYRFCg3zfkmBt_BifsNABbENYMjL54FsSQ"
    }
    response = client.post('/user/register', json=data)
    dataLogin = {
        "email": "test3@gmail.com",
        "password": "test123",
    }
    responseLogin = client.post('/user/login', json=dataLogin)
    token = responseLogin.json['token']
    response = client.get('/enterprise/currentEnterprise', headers={"Authorization": token})
    assert response.status_code == 404

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