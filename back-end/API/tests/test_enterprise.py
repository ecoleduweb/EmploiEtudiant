import pytest
from app import create_app, db
from app.models.enterprise_model import Enterprise
from app.models.user_model import User
from app.models.city_model import City
from app.models.region_model import Region
from argon2 import PasswordHasher
from freezegun import freeze_time

hasher = PasswordHasher()
user_with_enterprise = {
    'verified': False,
    "id": 2,
    "firstName": "No enterprise",
    "lastName": "test",
    "email": "no@enterprise.com",
    "isModerator": True,
    "active": True,
    "enterpriseId": 2
}
user_without_enterprise ={
    'verified': False,
    "id": 3,
    "firstName": "has enterprise",
    "lastName": "test",
    "email": "has@enterprise.com",
    "isModerator": True,
    "active": True,
    "enterpriseId": None
}

user_with_enterprise_id_1 = {
    'verified': False,
    "id": 1,
    "firstName": "test",
    "lastName": "test",
    "email": "test@test.com",
    "isModerator": True,
    "active": True,
    "enterpriseId": 1
}

@pytest.fixture(scope='module', autouse=True)
def freeze_test_date():
    with freeze_time("2021-11-15"):
        yield

@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        db.session.add(Region(
            id=1,
            region="Bas-Saint-Laurent"
        ))

        db.session.add(City(
            id=1,
            city="St-antoine-du-demi-dieu",
            idRegion=1,
        ))

        db.session.add(City(
            id=2,
            city="juste-st-antoine",
            idRegion=1,
        ))

        enterprise = Enterprise(**{
            "id": 1,
            "name": "entreprise 1",
            "email": "test@test.com",
            "phone": "123-123-1234",
            "address": "123 rue de la",
            "isTemporary": False,
            "cityId": 1,
        })
        db.session.add(enterprise)
        enterprise = Enterprise(**{
            "id": 2,
            "name": "enterprise 2",
            "email": "test2@test.com",
            "phone": "123-123-1234",
            "address": "123 rue de la",
            "isTemporary": True,
            "cityId": 1,
        })
        db.session.add(enterprise)
        hashed_password = hasher.hash("test123_12caracters!")
        user= User(**user_with_enterprise_id_1)
        user.password = hashed_password
        db.session.add(user)
        db.session.add(User(**user_with_enterprise))
        db.session.add(User(**user_without_enterprise))
        db.session.commit()
        
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    with app.test_client() as client:
        dataLogin = {
            "email": "test@test.com",
            "password": "test123_12caracters!",
        }
        res= client.post('/auth/login', json=dataLogin)
        assert res.status_code == 200
        yield client
  

def test_getEnterprises(client):
    response = client.get('/enterprise/all')
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
    response = client.post('/enterprise/new', json=data)
    assert response.status_code == 201
    assert response.json == {
        "address":"123 rue de la",
        "city":{
            "city":"St-antoine-du-demi-dieu",
            "id":1,
            "idRegion":1
        },
        "cityId":1,
        "email":"testTest@gmail.com",
        "id":3,
        "isTemporary":False,
        "name":"Développeur",
        "phone":"123-123-1234",
        "users": []
    }

def test_getEnterprise(client):
    response = client.get('/enterprise/1')
    assert response.status_code == 200
    assert response.json == {
        'address': '123 rue de la', 
        'city': 
            {'city': 
             'St-antoine-du-demi-dieu', 
             'id': 1, 
             'idRegion': 1
            }, 
        'cityId': 1, 
        'email': 'test@test.com', 
        'id': 1, 
        'isTemporary': False, 
        'name': 'entreprise 1', 
        'phone': '123-123-1234',
        "users": [user_with_enterprise_id_1]
        }

def test_checkIfUserHaveEnterprise(client):
    response = client.get('/enterprise/currentEnterprise')
    assert response.status_code == 200
    assert response.json == {
    'address': '123 rue de la', 
    'city': 
        {'city': 
            'St-antoine-du-demi-dieu', 
            'id': 1, 
            'idRegion': 1
        }, 
    'cityId': 1, 
    'email': 'test@test.com', 
    'id': 1, 
    'isTemporary': False, 
    'name': 'entreprise 1', 
    'phone': '123-123-1234',
    'users': [user_with_enterprise_id_1]
    }



def test_updateEnterprise(client):
    data = {
        "id": 2,
        "name": "nom modifié",
        "email": "mod@test.com",
        "phone": "123-123-2222",
        "address": "123 rue de la",
        "cityId": 2,
        "users": [
            user_without_enterprise,
        ]
    }
    response = client.put('/enterprise/2', json=data)
    assert response.status_code == 200
    assert response.json == {
        "address":"123 rue de la",
        "city":{
            "city":"juste-st-antoine",
            "id":2,
            "idRegion":1
        },
        "cityId":2,
        "email":"mod@test.com",
        "id":2,
        "isTemporary":False,
        "name":"nom modifié",
        "phone":"123-123-2222",
        "users": [{
            'verified': False,
            "id": 3,
            "firstName": "has enterprise",
            "lastName": "test",
            "email": "has@enterprise.com",
            "isModerator": True,
            "active": True,
            "enterpriseId": 2
        }]
    }
 
def test_checkIfUserHaveEnterprise_NewUser(client):
    data = {
        "id": 2,
        "firstName":"Test", 
        "lastName":"NouveauUser",
        "email": "test3@gmail.com",
        "password": "test123_12caracters!",
        "role": "user",
        "captchaToken": "03AFcWeA6bh39D5UeY9TN5C72LTE_VrIteCxQWvc0TCa2sErSF56PlrAZ3oFo5WSnaRxHnlJ3MUBm0KlhWeNs57_tq6nbFKON-DQFP3G5KyQZ5wfLb6fVKmwiyAqop77TrVOKr2B5e-mpYwyYzahOcv-AAUmFimWECWwqJqgBIIky758YeIer6XB5QsNqPeFrEDqR4bnBQiArqzguQsPu0QBs02XYtcnVc97HjUOTELPCCFtId18D6ZPvlVXYFarxffP4OkadMRZIApLd5vQOKfjj-RW9IdPCAtBDll_6k5WJiLCHQmEgkXrnEQOddTg8oaC7AeZS4q7sTTu_5QwBGi5fLbDt2i-8Xt6MQ3Jw-W97PZgAhAoywA1UmnqkhaVksnBJs4Ya_J7Hp5XY6WDSq9ngDeYCEPXXXrqWmY4H056dR8LvKzxIrtKHtjV4gEDbnGKS0m8NxmsiulMExZN-ABUI61uw8TQr8Y0Jg8mwGBnmXReg3ZVTr-LUIq-b-0rt6RTAKnY5ow2kEfAah9L0EhFcbcnM6FK1OM5ecL48bDVEWfOBMx8sSIUYsl85SogguOx8fN7ntIzVM3gCqWfcoPraPvC08rzDcaBJg9PmwMhDOkTgYDyWOwV4jrcbB_lK4quGjt_M-rynHLUIsDw49Yy4mNZuPXzAd1yxi-stlRU7ZCpYQAfw73bl4IF_stnRkEtosWUOkhlHRDJMQ7Dk9KbDn7_-cmCHnFc2I6mGBAhU2DV7RJxZE21DsOFtP6qc8N-HnMpQhEzv6Fbq_iQ6pPmB3Qm_rSvvAtPbW_AxR1wm-sqjFtNt51-sAXRYQMP70co1f2rWtb7pJL9j_FRnubjTmiGWKZX-qnMEL2RIZXuu8uONLe24F1KKz7F60_HRjC5QHEqXHKpxY7bHNp4eLsTKhFBGkrObt92K8GJfbJe5XS2sXae2rsaDtUcUu1U1DkagcM_3UgxBYQtxVzix57nge4W0_wEBJo9nQfXApBZCm9myL0ldwGuw9gQn1QnXzndlppKQa0_tUGYqnoLLwer6NzmwcxhxCLoAnLVYeXAt6xBzK3X1JsHIanjwxwZe1UNy372CRpKH1iRdqbX6jtcJyJbGRRjS7Ho28axdT-wXCEl0f2mAhL-VbXJ_Y4mwHzik8UTbJdMpLEFqr3ePT7yDFlWCBAD6VMDTlwarLHvOmqwB7t0IV_CFXeFL6YSalqvxuM3OcZftUUFRn0DMcs85eVDScWmTm89u83-6K0_NpA58vk0R2nL9ojsD5neKr1fauxnBbn5LSlxtA79RdLp0GxdCbmnxzdE_G1AibpepXCFeHgEojMWV7Qhk0Tph7WnYVGylz0LPqSNos22KrGfvf2yTmLnN-joAuuicbX4c_A6T-eqI7liTD-i_NTalgg7oumlw5C6XgPLgquJ522ueKbJLey_02GgLOhIvUAsl0WE7ZjgklQPo4QBfsybztmJbZnEuVgDZQnhPZzJH6ZE8H-snYoFoZmL3vQKZ_uVLqWrC1JJNyZgFxND2A66IhRZXp4NWTd5olcuk2ZuffRWTjJnJ_DD8G4ETCpOGocUb6YN23xOxaZS66il_Ej_U63DEopFEBgsRuJlzY_k5iX1RLuQQObUj-XO_alhCTi7KejjbJatFigDzc-gtj-t3RrHCWSwKqcOvM6FUt56NS12P5NNN2ROJ-LKh-iCdBHj8wbvm6_MPZJParB2fi3W0DbY7PPkUPmYCtqjHYcESZpbkc2l2fJNlmqYqkOUOahTAJL3kWgFvXuku0Ec5GDWhdEaT1WBQmwJGWh49f0olkGr3qI0k1oJc4c0kV_3byYaYq9y58M_9wV4oBgIFCNirJe-Es9kqRX3uE3ONicGclV8KT_0cFZveNSyIAeiIHPrtO4zU6qxXJz_J1lKRwPXFvD5QlpqilknMpQW5dJOEOgLim7WlXnbEEYd38Whj5Y_ZvuSgzTr8y75s2_XVI7FPStYRFCg3zfkmBt_BifsNABbENYMjL54FsSQ"
    }
    response = client.post('/auth/register', json=data)
    dataLogin = {
       "email": "test3@gmail.com",
       "password": "test123_12caracters!",
    }
    client.post('/auth/login', json=dataLogin)
    response = client.get('/enterprise/currentEnterprise')
    assert response.status_code == 404