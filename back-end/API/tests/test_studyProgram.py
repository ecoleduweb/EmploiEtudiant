import os
import pytest
from app import create_app, db
from app.models.study_program_model import StudyProgram

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
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

def studyPrograms(client):
    response = client.get('/studyPrograms')
    assert response.status_code == 200
    assert len(response.json) == 2

def studyProgramId(client):
    response = client.get('/studyProgramId?name=Informatique')
    assert response.status_code == 200
    assert response.json == 1

def addStudyProgram(client):
    data = {
        "name": "Génie logiciel"
    }
    response = client.post('/addStudyProgram', json=data)
    assert response.status_code == 200
    assert response.json == {
        "id": 3,
        "name": "Génie logiciel"
    }