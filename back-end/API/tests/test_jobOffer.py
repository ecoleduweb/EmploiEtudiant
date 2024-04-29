import pytest
from app import create_app, db
from app.models.jobOffer_model import JobOffer
from app.models.user_model import User
from app.models.study_program_model import StudyProgram
from app.models.employmentSchedule_model import EmploymentSchedule

from argon2 import PasswordHasher

hasher = PasswordHasher()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        job_offer1_data = {
            "id": 1,
            "title": "Développeur",
            "address": "123 rue de la rue",
            "description": "Développeur fullstack",
            "dateEntryOffice": "2021-12-12",
            "deadlineApply": "2021-12-12",
            "email": "test@gmail.com",
            "hoursPerWeek": 40,
            "compliantEmployer": True,
            "internship": False,
            "offerLink": "www.google.com",
            "salary": 1000,
            "offerDebut": "2021-12-12",
            "active": True,
            "approbationMessage": "Super offre!",
            "employerId": None,
            "scheduleId": None,
            "isApproved": True
        }
        job_offer = JobOffer(**job_offer1_data)
        db.session.add(job_offer)
        job_offer2_data = {
            "id": 2,
            "title": "Développeur",
            "address": "123 rue de la rue",
            "description": "Développeur front-end",
            "dateEntryOffice": "2021-12-12",
            "deadlineApply": "2021-12-12",
            "email": "test@gmail.com",
            "hoursPerWeek": 40,
            "compliantEmployer": True,
            "internship": False,
            "offerLink": "www.google.com",
            "salary": 1000,
            "offerDebut": "2021-12-12",
            "active": True,
            "employerId": None,
            "scheduleId": None,
            "isApproved": False
        }
        job_offer2 = JobOffer(**job_offer2_data)
        db.session.add(job_offer2)
        hashed_password = hasher.hash("test123")
        user = User(id=1, firstName="Robert", lastName="Lizotte", email="test@gmail.com", password=hashed_password, active=True, isModerator=False)
        admin = User(id=2, firstName="Joe", lastName="Baril", email="bigJoeDu91@cegeprdl.ca", password=hashed_password, active=True, isModerator=True)
        db.session.add(admin)
        db.session.add(user)
        studyProgram1_data = {
            "id": 1,
            "name": "Informatique"
        }
        studyProgram1_data = StudyProgram(**studyProgram1_data)
        db.session.add(studyProgram1_data)
        studyProgram2_data = {
            "id": 2,
            "name": "Génie logiciel"
        }
        studyProgram2_data = StudyProgram(**studyProgram2_data)
        db.session.add(studyProgram2_data)
        employmentSchedule1_data = {
            "id": 1,
            "description": "Temps plein"
        }
        employmentSchedule1_data = EmploymentSchedule(**employmentSchedule1_data)
        db.session.add(employmentSchedule1_data)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


def test_offreEmploi(client):
    response = client.get('/jobOffer/offreEmploi?id=1')
    print(response.json)
    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "title": "Développeur",
        "address": "123 rue de la rue",
        "description": "Développeur fullstack",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2021-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": 40,
        "compliantEmployer": True,
        "internship": False,
        "offerLink": "www.google.com",
        "salary": "1000",
        "offerDebut": "2021-12-12",
        "active": True,
        "approbationMessage": "Super offre!",
        "employerId": None,
        "scheduleId": None,
        "isApproved": True
    }

def test_offresEmploi(client):
    data1 = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    responseLogin = client.post('/user/login', json=data1)
    token = responseLogin.json['token']
    response = client.get('/jobOffer/offresEmploi', headers={'Authorization': token})
    print(response)
    assert response.status_code == 200
    assert len(response.json) == 2

def test_userCreateOffresEmploi(client):
    data = {
            "jobOffer": 
            {
                "title": "Développeur",
                "address": "123 rue de la rue",
                "description": "Développeur front-end",
                "dateEntryOffice": "2021-12-12",
                "deadlineApply": "2021-12-12",
                "email": "test@gmail.com",
                "hoursPerWeek": 40,
                "compliantEmployer": True,
                "internship": False,
                "offerLink": "www.google.com",
                "salary": 1000,
                "offerDebut": "2021-12-12",
                "active": True,
                "employerId": 1,
                "scheduleId": 1,
                "isApproved": False
            },
            "enterprise": 
            {
                "id": 1,
                "name": "Google",
                "email": "google@gmail.com",
                "phone": "1234567890",
                "address": "123 rue google",
                "cityId": 1
            },
            "studyPrograms": [
                "Informatique",
                "Génie logiciel"
            ]
        }
    data1 = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    responseLogin = client.post('/user/login', json=data1)
    token = responseLogin.json['token']
    response = client.post('/jobOffer/createJobOffer', json=data, headers={'Authorization': token})
    assert response.status_code == 200

def test_approveJobOffer(client):
    data = {
        "id": 1,
        "approbationMessage": "Super offre!",
        "isApproved": True
    }
    data1 = {
        "email": "bigJoeDu91@cegeprdl.ca",
        "password": "test123"
    }
    responseLogin = client.post('/user/login', json=data1)
    token = responseLogin.json['token']
    print(responseLogin.json)
    response = client.put('/jobOffer/approveJobOffer', json=data, headers={'Authorization': token})
    assert response.status_code == 200