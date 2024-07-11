import os
import pytest
from argon2 import PasswordHasher
from jwt import decode
from app import create_app, db
from app.models.user_model import User 

hasher = PasswordHasher()

@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        hashed_password = hasher.hash("test123")
        user = User(id=1, firstName="Robert", lastName="Lizotte", email="test@gmail.com", password=hashed_password, active=True, isModerator=False)  # Removed 'name' attribute
        db.session.add(user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

def test_register(client):
    data = {
        "id": 2,
        "firstName":"Robert", 
        "lastName":"Lizotte",
        "email": "test2@gmail.com",
        "password": "test123",
        "role": "user",
        "captchaToken": "03AFcWeA6bh39D5UeY9TN5C72LTE_VrIteCxQWvc0TCa2sErSF56PlrAZ3oFo5WSnaRxHnlJ3MUBm0KlhWeNs57_tq6nbFKON-DQFP3G5KyQZ5wfLb6fVKmwiyAqop77TrVOKr2B5e-mpYwyYzahOcv-AAUmFimWECWwqJqgBIIky758YeIer6XB5QsNqPeFrEDqR4bnBQiArqzguQsPu0QBs02XYtcnVc97HjUOTELPCCFtId18D6ZPvlVXYFarxffP4OkadMRZIApLd5vQOKfjj-RW9IdPCAtBDll_6k5WJiLCHQmEgkXrnEQOddTg8oaC7AeZS4q7sTTu_5QwBGi5fLbDt2i-8Xt6MQ3Jw-W97PZgAhAoywA1UmnqkhaVksnBJs4Ya_J7Hp5XY6WDSq9ngDeYCEPXXXrqWmY4H056dR8LvKzxIrtKHtjV4gEDbnGKS0m8NxmsiulMExZN-ABUI61uw8TQr8Y0Jg8mwGBnmXReg3ZVTr-LUIq-b-0rt6RTAKnY5ow2kEfAah9L0EhFcbcnM6FK1OM5ecL48bDVEWfOBMx8sSIUYsl85SogguOx8fN7ntIzVM3gCqWfcoPraPvC08rzDcaBJg9PmwMhDOkTgYDyWOwV4jrcbB_lK4quGjt_M-rynHLUIsDw49Yy4mNZuPXzAd1yxi-stlRU7ZCpYQAfw73bl4IF_stnRkEtosWUOkhlHRDJMQ7Dk9KbDn7_-cmCHnFc2I6mGBAhU2DV7RJxZE21DsOFtP6qc8N-HnMpQhEzv6Fbq_iQ6pPmB3Qm_rSvvAtPbW_AxR1wm-sqjFtNt51-sAXRYQMP70co1f2rWtb7pJL9j_FRnubjTmiGWKZX-qnMEL2RIZXuu8uONLe24F1KKz7F60_HRjC5QHEqXHKpxY7bHNp4eLsTKhFBGkrObt92K8GJfbJe5XS2sXae2rsaDtUcUu1U1DkagcM_3UgxBYQtxVzix57nge4W0_wEBJo9nQfXApBZCm9myL0ldwGuw9gQn1QnXzndlppKQa0_tUGYqnoLLwer6NzmwcxhxCLoAnLVYeXAt6xBzK3X1JsHIanjwxwZe1UNy372CRpKH1iRdqbX6jtcJyJbGRRjS7Ho28axdT-wXCEl0f2mAhL-VbXJ_Y4mwHzik8UTbJdMpLEFqr3ePT7yDFlWCBAD6VMDTlwarLHvOmqwB7t0IV_CFXeFL6YSalqvxuM3OcZftUUFRn0DMcs85eVDScWmTm89u83-6K0_NpA58vk0R2nL9ojsD5neKr1fauxnBbn5LSlxtA79RdLp0GxdCbmnxzdE_G1AibpepXCFeHgEojMWV7Qhk0Tph7WnYVGylz0LPqSNos22KrGfvf2yTmLnN-joAuuicbX4c_A6T-eqI7liTD-i_NTalgg7oumlw5C6XgPLgquJ522ueKbJLey_02GgLOhIvUAsl0WE7ZjgklQPo4QBfsybztmJbZnEuVgDZQnhPZzJH6ZE8H-snYoFoZmL3vQKZ_uVLqWrC1JJNyZgFxND2A66IhRZXp4NWTd5olcuk2ZuffRWTjJnJ_DD8G4ETCpOGocUb6YN23xOxaZS66il_Ej_U63DEopFEBgsRuJlzY_k5iX1RLuQQObUj-XO_alhCTi7KejjbJatFigDzc-gtj-t3RrHCWSwKqcOvM6FUt56NS12P5NNN2ROJ-LKh-iCdBHj8wbvm6_MPZJParB2fi3W0DbY7PPkUPmYCtqjHYcESZpbkc2l2fJNlmqYqkOUOahTAJL3kWgFvXuku0Ec5GDWhdEaT1WBQmwJGWh49f0olkGr3qI0k1oJc4c0kV_3byYaYq9y58M_9wV4oBgIFCNirJe-Es9kqRX3uE3ONicGclV8KT_0cFZveNSyIAeiIHPrtO4zU6qxXJz_J1lKRwPXFvD5QlpqilknMpQW5dJOEOgLim7WlXnbEEYd38Whj5Y_ZvuSgzTr8y75s2_XVI7FPStYRFCg3zfkmBt_BifsNABbENYMjL54FsSQ"
    }
    dataLogin = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    reponseLogin = client.post('/user/login', json=dataLogin)
    token = reponseLogin.json['token']
    response = client.post('/user/register', json=data, headers={"Authorization": token})
    assert response.status_code == 200

def test_update(client):

    #Utilisateur normale

    #Connexion initiale
    data1 = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    response1 = client.post('/user/login', json=data1)
    assert response1.status_code == 200
    assert 'token' in response1.json

    token = response1.json['token']

    data = decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
    assert data["email"] != "" or data["email"] != " " 

    #Changement de l'utilisateur
    data2 = {
        "email": "test@gmail.com",
        "firstname": "TEST123",
        "lastname": "TEST123"
    }
    response2 = client.put('/user/updateUser', json=data2, headers={"Authorization": token})
    assert response2.status_code == 200

    #Reconnexion
    data3 = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    response3 = client.post('/user/login', json=data3)
    assert response3.status_code == 200
    assert 'token' in response3.json

    token = response3.json['token']

    data = decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
    assert data["email"] != "" or data["email"] != " "

    assert data["lastName"] == "TEST123"

    #Administrateur

    #Ajout d'utilisateur administrateur
    hashed_password = hasher.hash("test123")
    user = User(id=4, firstName="admin2", lastName="admin2", email="admin2@gmail.com", password=hashed_password, active=True, isModerator=True)
    db.session.add(user)
    db.session.commit()

    #Ajout d'un autre utilisteur (non admin)
    hashed_password = hasher.hash("test123")
    user = User(id=5, firstName="pierre", lastName="Pierre", email="pierre@gmail.com", password=hashed_password, active=True, isModerator=False)
    db.session.add(user)
    db.session.commit()

    #Connexion initiale
    data1 = {
        "email": "admin2@gmail.com",
        "password": "test123"
    }
    response1 = client.post('/user/login', json=data1)
    assert response1.status_code == 200
    assert 'token' in response1.json

    token = response1.json['token']

    #Changement de l'utilisateur
    data2 = {
        "email": "pierre@gmail.com",
        "firstname": "TEST1234",
        "lastname": "TEST1234"
    }
    response2 = client.put('/user/updateUser', json=data2, headers={"Authorization": token})
    assert response2.status_code == 200

    #Connexion de l'utilisateur
    data3 = {
        "email": "pierre@gmail.com",
        "password": "test123"
    }
    response3 = client.post('/user/login', json=data3)
    assert response3.status_code == 200
    assert 'token' in response3.json

    token2 = response3.json['token']

    data = decode(token2, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
    assert data["email"] != "" or data["email"] != " " 

    assert data["lastName"] == "TEST1234"

def test_resetPassword(client):

    #Utilisateur normale

    #Connexion initiale
    data1 = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    response1 = client.post('/user/login', json=data1)
    assert response1.status_code == 200
    assert 'token' in response1.json

    token = response1.json['token']

    #Changement de mot de passe
    data2 = {
        "email": "test@gmail.com",
        "password": "test1234"
    }
    response2 = client.put('/user/updatePassword', json=data2, headers={"Authorization": token})
    assert response2.status_code == 200

    #Connexion avec le mot de passe modifié
    data3 = {
        "email": "test@gmail.com",
        "password": "test1234"
    }
    response3 = client.post('/user/login', json=data3)
    assert response3.status_code == 200
    assert 'token' in response3.json

    token2 = response3.json['token']

    #Remodification du mot de passe
    data2 = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    response4 = client.put('/user/updatePassword', json=data2, headers={"Authorization": token2})
    assert response4.status_code == 200


    #Administrateur

    #Ajout d'utilisateur administrateur
    hashed_password = hasher.hash("test123")
    user = User(id=3, firstName="admin", lastName="admin", email="admin@gmail.com", password=hashed_password, active=True, isModerator=True)
    db.session.add(user)
    db.session.commit()

    #Connexion initiale
    data1 = {
        "email": "admin@gmail.com",
        "password": "test123"
    }
    response1 = client.post('/user/login', json=data1)
    assert response1.status_code == 200
    assert 'token' in response1.json

    token = response1.json['token']

    #Changement de mot de passe (avec token admin)
    data2 = {
        "email": "test@gmail.com",
        "password": "test1234"
    }
    response2 = client.put('/user/updatePassword', json=data2, headers={"Authorization": token})
    assert response2.status_code == 200

    #Connexion avec le mot de passe modifié
    data3 = {
        "email": "test@gmail.com",
        "password": "test1234"
    }
    response3 = client.post('/user/login', json=data3)
    assert response3.status_code == 200
    assert 'token' in response3.json

    token2 = response3.json['token']

    #Remodification du mot de passe (avec token admin)
    data2 = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    response4 = client.put('/user/updatePassword', json=data2, headers={"Authorization": token})
    assert response4.status_code == 200


def test_login(client):
    data = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    response = client.post('/user/login', json=data)
    assert response.status_code == 200
    assert 'token' in response.json
