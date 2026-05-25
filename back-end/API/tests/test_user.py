import os
import pytest
from argon2 import PasswordHasher
from jwt import decode
from app import create_app, db
from app.models.user_model import User 
from freezegun import freeze_time

hasher = PasswordHasher()

@pytest.fixture(scope='module', autouse=True)
def freeze_test_date():
    with freeze_time("2021-11-15"):
        yield

@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        hashed_password = hasher.hash("test123_12caracters!")
        user = User(id=1, firstName="Robert", lastName="Lizotte", email="test@gmail.com", password=hashed_password, active=True, isModerator=False)  # Removed 'name' attribute
        db.session.add(user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
   with app.test_client() as client:
        yield client

def test_register(client):
    data = {
        "id": 2,
        "firstName":"Robert", 
        "lastName":"Lizotte",
        "email": "test2@gmail.com",
        "password": "test123_12caracters!",
        "role": "user",
        "captchaToken": "03AFcWeA6bh39D5UeY9TN5C72LTE_VrIteCxQWvc0TCa2sErSF56PlrAZ3oFo5WSnaRxHnlJ3MUBm0KlhWeNs57_tq6nbFKON-DQFP3G5KyQZ5wfLb6fVKmwiyAqop77TrVOKr2B5e-mpYwyYzahOcv-AAUmFimWECWwqJqgBIIky758YeIer6XB5QsNqPeFrEDqR4bnBQiArqzguQsPu0QBs02XYtcnVc97HjUOTELPCCFtId18D6ZPvlVXYFarxffP4OkadMRZIApLd5vQOKfjj-RW9IdPCAtBDll_6k5WJiLCHQmEgkXrnEQOddTg8oaC7AeZS4q7sTTu_5QwBGi5fLbDt2i-8Xt6MQ3Jw-W97PZgAhAoywA1UmnqkhaVksnBJs4Ya_J7Hp5XY6WDSq9ngDeYCEPXXXrqWmY4H056dR8LvKzxIrtKHtjV4gEDbnGKS0m8NxmsiulMExZN-ABUI61uw8TQr8Y0Jg8mwGBnmXReg3ZVTr-LUIq-b-0rt6RTAKnY5ow2kEfAah9L0EhFcbcnM6FK1OM5ecL48bDVEWfOBMx8sSIUYsl85SogguOx8fN7ntIzVM3gCqWfcoPraPvC08rzDcaBJg9PmwMhDOkTgYDyWOwV4jrcbB_lK4quGjt_M-rynHLUIsDw49Yy4mNZuPXzAd1yxi-stlRU7ZCpYQAfw73bl4IF_stnRkEtosWUOkhlHRDJMQ7Dk9KbDn7_-cmCHnFc2I6mGBAhU2DV7RJxZE21DsOFtP6qc8N-HnMpQhEzv6Fbq_iQ6pPmB3Qm_rSvvAtPbW_AxR1wm-sqjFtNt51-sAXRYQMP70co1f2rWtb7pJL9j_FRnubjTmiGWKZX-qnMEL2RIZXuu8uONLe24F1KKz7F60_HRjC5QHEqXHKpxY7bHNp4eLsTKhFBGkrObt92K8GJfbJe5XS2sXae2rsaDtUcUu1U1DkagcM_3UgxBYQtxVzix57nge4W0_wEBJo9nQfXApBZCm9myL0ldwGuw9gQn1QnXzndlppKQa0_tUGYqnoLLwer6NzmwcxhxCLoAnLVYeXAt6xBzK3X1JsHIanjwxwZe1UNy372CRpKH1iRdqbX6jtcJyJbGRRjS7Ho28axdT-wXCEl0f2mAhL-VbXJ_Y4mwHzik8UTbJdMpLEFqr3ePT7yDFlWCBAD6VMDTlwarLHvOmqwB7t0IV_CFXeFL6YSalqvxuM3OcZftUUFRn0DMcs85eVDScWmTm89u83-6K0_NpA58vk0R2nL9ojsD5neKr1fauxnBbn5LSlxtA79RdLp0GxdCbmnxzdE_G1AibpepXCFeHgEojMWV7Qhk0Tph7WnYVGylz0LPqSNos22KrGfvf2yTmLnN-joAuuicbX4c_A6T-eqI7liTD-i_NTalgg7oumlw5C6XgPLgquJ522ueKbJLey_02GgLOhIvUAsl0WE7ZjgklQPo4QBfsybztmJbZnEuVgDZQnhPZzJH6ZE8H-snYoFoZmL3vQKZ_uVLqWrC1JJNyZgFxND2A66IhRZXp4NWTd5olcuk2ZuffRWTjJnJ_DD8G4ETCpOGocUb6YN23xOxaZS66il_Ej_U63DEopFEBgsRuJlzY_k5iX1RLuQQObUj-XO_alhCTi7KejjbJatFigDzc-gtj-t3RrHCWSwKqcOvM6FUt56NS12P5NNN2ROJ-LKh-iCdBHj8wbvm6_MPZJParB2fi3W0DbY7PPkUPmYCtqjHYcESZpbkc2l2fJNlmqYqkOUOahTAJL3kWgFvXuku0Ec5GDWhdEaT1WBQmwJGWh49f0olkGr3qI0k1oJc4c0kV_3byYaYq9y58M_9wV4oBgIFCNirJe-Es9kqRX3uE3ONicGclV8KT_0cFZveNSyIAeiIHPrtO4zU6qxXJz_J1lKRwPXFvD5QlpqilknMpQW5dJOEOgLim7WlXnbEEYd38Whj5Y_ZvuSgzTr8y75s2_XVI7FPStYRFCg3zfkmBt_BifsNABbENYMjL54FsSQ"
    }
    
    response = client.post('/auth/register', json=data)
    assert response.status_code == 200

def test_updateUserNormal(client):
    #Utilisateur normale

    #Connexion initiale
    data1 = {
        "email": "test@gmail.com",
        "password": "test123_12caracters!"
    }
    response1 = client.post('/auth/login', json=data1)
    assert response1.status_code == 200
   
    #Changement de l'utilisateur
    data2 = {
        "id": 1,
        "email": "test3@gmail.com",
        "firstName": "TEST123",
        "lastName": "TEST123"
    }
    response2 = client.put('/user/1', json=data2)
    assert response2.status_code == 200

    #Reconnexion
    data3 = {
        "email": "test3@gmail.com",
        "password": "test123_12caracters!"
    }
    response3 = client.post('/auth/login', json=data3)
    assert response3.status_code == 200

    #Changement de l'utilisateur pour le reste des tests
    data2 = {
        "id": 1,
        "email": "test@gmail.com",
        "firstName": "TEST123",
        "lastName": "TEST123"
    }
    response2 = client.put('/user/1', json=data2)
    assert response2.status_code == 200

def test_updateUserAdmin(client):
    #Administrateur

    #Ajout d'utilisateur administrateur
    hashed_password = hasher.hash("test123_12caracters!")
    user = User(id=4, firstName="admin2", lastName="admin2", email="admin2@gmail.com", password=hashed_password, active=True, isModerator=True)
    db.session.add(user)
    db.session.commit()

    #Ajout d'un autre utilisteur (non admin)
    hashed_password = hasher.hash("test123_12caracters!")
    user = User(id=5, firstName="pierre", lastName="Pierre", email="pierre@gmail.com", password=hashed_password, active=True, isModerator=False)
    db.session.add(user)
    db.session.commit()

    #Connexion initiale
    data1 = {
        "email": "admin2@gmail.com",
        "password": "test123_12caracters!"
    }
    response1 = client.post('/auth/login', json=data1)
    assert response1.status_code == 200
   
    #Changement de l'utilisateur
    data2 = {
        "id" : 5,
        "email": "pierre@gmail.com",
        "firstName": "TEST1234",
        "lastName": "TEST1234"
    }
    response2 = client.put('/user/5', json=data2)
    assert response2.status_code == 200

    #Connexion de l'utilisateur
    data3 = {
        "email": "pierre@gmail.com",
        "password": "test123_12caracters!"
    }
    response3 = client.post('/auth/login', json=data3)
    assert response3.status_code == 200
   

def test_resetPasswordNormal(client):
    #Utilisateur normale

    #Connexion initiale
    data1 = {
        "email": "test2@gmail.com",
        "password": "test123_12caracters!"
    }
    response1 = client.post('/auth/login', json=data1)
    assert response1.status_code == 200
   

    #Changement de mot de passe
    data2 = {
        "email": "test2@gmail.com",
        "password": "nouvveau_caracters!!"
    }
    response2 = client.put('/auth/updatePassword/2', json=data2)
    assert response2.status_code == 200

    #Connexion avec le mot de passe modifié
    data3 = {
        "email": "test2@gmail.com",
        "password": "nouvveau_caracters!!"
    }
    response3 = client.post('/auth/login', json=data3)
    assert response3.status_code == 200
   
def test_restPasswordWrongUser(client):
    # connexion initiale
    data1 = {
        "email": "test@gmail.com",
        "password": "test123_12caracters!"
    }
    response1 = client.post('/auth/login', json=data1)
    assert response1.status_code == 200
    #Modification du mot de passe avec courriel d'un autre utilisateur/invalide
    data = {
        "email": "test2@gmail.com",
        "password": "test123_12caracters!!!"
    }
    response4 = client.put('/auth/updatePassword/2', json=data)
    assert response4.status_code == 403

def test_resetPasswordAdmin(client):
    #Administrateur

    #Ajout d'utilisateur administrateur
    hashed_password = hasher.hash("test123_12caracters!")
    user = User(id=3, firstName="admin", lastName="admin", email="admin@gmail.com", password=hashed_password, active=True, isModerator=True)
    db.session.add(user)
    db.session.commit()

    #Connexion initiale
    data1 = {
        "email": "admin@gmail.com",
        "password": "test123_12caracters!"
    }
    response1 = client.post('/auth/login', json=data1)
    assert response1.status_code == 200
   
    #Changement de mot de passe (avec token admin)
    data2 = {
        "email": "test@gmail.com",
        "password": "test123_12caracters!!"
    }
    response2 = client.put('/auth/updatePassword/1', json=data2)
    assert response2.status_code == 200

    #Connexion avec le mot de passe modifié
    data3 = {
        "email": "test@gmail.com",
        "password": "test123_12caracters!!"
    }
    response3 = client.post('/auth/login', json=data3)
    assert response3.status_code == 200
   
    #Remodification du mot de passe (avec token admin)
    data2 = {
        "email": "test@gmail.com",
        "password": "test123_12caracters!"
    }
    response4 = client.put('/auth/updatePassword/1', json=data2)
    assert response4.status_code == 200

def test_makeAdmin(client):
    #Ajout d'utilisateur administrateur
    hashed_password = hasher.hash("test123_12caracters!")
    admin = User(id=6, firstName="admin3", lastName="admin3", email="admin3@gmail.com", password=hashed_password, active=True, isModerator=True)
    db.session.add(admin)

    #Ajout d'utilisateur utilisateur
    hashed_password = hasher.hash("test123_12caracters!")
    user_to_promote = User(id=7, firstName="utilisateur1", lastName="utilisateur1", email="utilisateur1@gmail.com", password=hashed_password, active=True, isModerator=False)
    db.session.add(user_to_promote)

    db.session.commit()

    #Connexion initiale
    data1 = {
        "email": "admin3@gmail.com",
        "password": "test123_12caracters!"
    }
    response1 = client.post('/auth/login', json=data1)
    assert response1.status_code == 200
    
    #Mettre l'utilisateur en admin
    data2 = {}
    response1 = client.put('/user/toggleAdmin/7', json=data2)
    assert response1.status_code == 200
    response = client.get('/user/7')
    assert response.status_code == 200
    assert response.json['isModerator'] == True


    assert user_to_promote.isModerator

    #Le remettre en non admin
    data2 = {
    }
    response1 = client.put('/user/toggleAdmin/7', json=data2)
    assert response1.status_code == 200
    response = client.get('/user/7')
    assert response.status_code == 200
    assert response.json['isModerator'] == False


def test_deleteUser(client):
    #Ajout d'utilisateur utilisateur
    hashed_password = hasher.hash("test123_12caracters!")
    user = User(id=8, firstName="utilisateur2", lastName="utilisateur2", email="utilisateur2@gmail.com", password=hashed_password, active=True, isModerator=False)
    db.session.add(user)
    db.session.commit()

    #Connexion initiale
    data1 = {
        "email": "admin3@gmail.com",
        "password": "test123_12caracters!"
    }
    response1 = client.post('/auth/login', json=data1)
    assert response1.status_code == 200
   
    #Supprimation de l'utilisateur 2
    data2 = {
        "email": "utilisateur2@gmail.com"
    }
    response1 = client.put(f'/user/delete/{user.id}', json=data2)

    data3 = {
        "email": "utilisateur2@gmail.com",
        "password": "test123_12caracters!"
    }
    response1 = client.post('/auth/login', json=data3)
    assert response1.status_code == 401


def test_desactivateUser(client):
    #Ajout d'utilisateur utilisateur
    hashed_password = hasher.hash("test123_12caracters!")
    user = User(id=8, firstName="utilisateur2", lastName="utilisateur2", email="utilisateur2@gmail.com", password=hashed_password, active=True, isModerator=False)
    db.session.add(user)
    db.session.commit()

    #Connexion initiale
    data1 = {
        "email": "admin3@gmail.com",
        "password": "test123_12caracters!"
    }
    response1 = client.post('/auth/login', json=data1)
    assert response1.status_code == 200
    
    #Désactivation de l'utilisateur 2
    data2 = {
        "email": "utilisateur2@gmail.com"
    }
    response1 = client.put(f'/user/toggleActive/{user.id}', json=data2)

    data3 = {
        "email": "utilisateur2@gmail.com",
        "password": "test123_12caracters!"
    }
    response1 = client.post('/auth/login', json=data3)
    assert response1.status_code == 403


def test_login(client):
    data = {
        "email": "test@gmail.com",
        "password": "test123_12caracters!"
    }
    response = client.post('/auth/login', json=data)
    assert response.status_code == 200
    
