import pytest
from app import create_app, db
from app.models.study_program_model import StudyProgram
from app.models.user_model import User
from argon2 import PasswordHasher

hasher = PasswordHasher()

@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        data_study_program1 = {
            "id": 1,
            "name": "Informatique"
        }
        study_program1 = StudyProgram(**data_study_program1)
        db.session.add(study_program1)
        data_study_program2 = {
            "id": 2,
            "name": "Gestion"
        }
        study_program2 = StudyProgram(**data_study_program2)
        db.session.add(study_program2)
        hashed_password = hasher.hash("test")
        data = {
            "id": 1,
            "email": "test@test.com",
            "firstName": "test",
            "lastName": "test",
            "password": hashed_password,
            "isModerator": True,
            "active": True,
        }
        user = User(**data)
        db.session.add(user)
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
        
  
def test_studyPrograms(client):
    response = client.get('/studyProgram/studyPrograms')
    assert response.status_code == 200
    assert len(response.json) == 2

def test_addStudyProgram(client):
    data = {
        "name": "Genie logiciel"
    }
    response = client.post('/studyProgram/new', json=data)
    assert response.status_code == 200

def test_editStudyProgram(client):
    data = {
        "name": "Informatiques"
    }
    response = client.put('/studyProgram/studyProgram/1', json=data)
    assert response.status_code == 200

def test_editStudyProgram_sameName(client):
    data = {
        "name": "Informatique"
    }
    client.put('/studyProgram/studyProgram/1', json=data)
    response = client.put('/studyProgram/studyProgram/1', json=data)
    assert response.status_code == 200