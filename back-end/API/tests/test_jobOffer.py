# test deploiment back-end
import pytest
from app import create_app, db
from app.models.jobOffer_model import JobOffer
from app.models.user_model import User
from app.models.enterprise_model import Enterprise
from app.models.employers_model import Employers
from app.models.study_program_model import StudyProgram
from app.models.employmentSchedule_model import EmploymentSchedule
from datetime import datetime

from argon2 import PasswordHasher

hasher = PasswordHasher()

job_offer1_data = {
    "id": 1,
    "title": "Développeur",
    "address": "123 rue de la rue",
    "description": "Développeur fullstack",
    "dateEntryOffice": "2021-12-12",
    "deadlineApply": "2121-12-12",
    "email": "test@gmail.com",
    "hoursPerWeek": 40,
    "offerLink": "www.google.com",
    "salary": "1000",
    "offerDebut": "2021-12-12",
    "active": True,
    "approbationMessage": "Super offre!",
    "employerId": 1,
    "isApproved": True,
    "approvedDate": datetime.now(),
    "last_modified_by_id": 1
}


def VerifyData(jobOfferData):
    for data in job_offer1_data:
        if (data not in jobOfferData) and (type(jobOfferData[data]) != type(job_offer1_data[data])) :
            return False

    return True


@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        enterprise_data = {
            "id": 1,
            "name": "Développeur",
            "email": "test@test.com",
            "phone": "123-123-1234",
            "address": "123 rue de la",
            "isTemporary": False,
            "cityId": 1,
        }
        enterprise = Enterprise(**enterprise_data)
        db.session.add(enterprise)
        employer_data = {
            "id": 1,
            "verified": True,
            "userId": None,
            "enterpriseId": 1,
        }
        employers = Employers(**employer_data)
        db.session.add(employers)
        job_offer = JobOffer(**job_offer1_data)
        db.session.add(job_offer)
        job_offer2_data = {
            "id": 2,
            "title": "Développeur",
            "address": "123 rue de la rue",
            "description": "Développeur front-end",
            "dateEntryOffice": "2021-12-12",
            "deadlineApply": "2121-12-12",
            "email": "test@gmail.com",
            "hoursPerWeek": 40,
            "offerLink": "www.google.com",
            "salary": '1000',
            "offerDebut": "2021-12-12",
            "active": True,
            "employerId": None,
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
    response = client.get('/jobOffer/1')
    assert response.status_code == 200
    assert VerifyData(response.json)

def test_offresEmploiApprouvees(client):
    data1 = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    responseLogin = client.post('/user/login', json=data1)
    token = responseLogin.json['token']
    response = client.get('/jobOffer/approved', headers={'Authorization': token})
    assert response.status_code == 200
    assert len(response.json) == 1

def test_offresEmploiApprouveesWithDetails(client):
    data1 = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    responseLogin = client.post('/user/login', json=data1)
    token = responseLogin.json['token']
    response = client.get('/jobOffer/approved?entrepriseDetails=true&employmentScheduleDetails=true&studyProgramDetails=true', headers={'Authorization': token})
    assert response.status_code == 200
    print(response.json[0])
    assert len(response.json) == 1
    assert response.json[0]['enterprise'] is not None
    assert response.json[0]['schedules'] is not None
    assert response.json[0]['studyPrograms'] is not None

def test_userCreateOffresEmploi(client):
    data = {
            "jobOffer": 
            job_offer1_data,
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
                1,
                2
            ],
            "scheduleIds": [
                1
            ]
        }
    data1 = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    responseLogin = client.post('/user/login', json=data1)
    token = responseLogin.json['token']
    response = client.post('/jobOffer/new', json=data, headers={'Authorization': token})
    assert response.status_code == 201

def test_adminCreateOffer(client):
    data = {
            "jobOffer": 
            job_offer1_data,
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
                1,
                2
            ],
            "scheduleIds": [
                1
            ]
        }
    
    data1 = {
        "email": "admin@gmail.com",
        "password": "test123"
    }

    data2 = {
        "id": 2,
        "name": "Netflix",
        "email": "netflix@gmail.com",
        "phone": "8888888888",
        "address": "14 rue de la rue",
        "cityId": 1,
        "isTemporary": True
    }


    hashed_password = hasher.hash("test123")
    user = User(id=3, firstName="admin", lastName="admin", email="admin@gmail.com", password=hashed_password, active=True, isModerator=True)
    db.session.add(user)
    db.session.commit()

    responseLogin = client.post('/user/login', json=data1)
    token = responseLogin.json['token']
    response = client.post('/jobOffer/new', json=data, headers={'Authorization': token})
    response2 = client.post('http://localhost:5000/enterprise/new', json=data2, headers={'Authorization': token})
    EmployerCount = client.get('/enterprise/all', headers={'Authorization': token})
    assert response.status_code == 201 and response2.status_code == 200 and EmployerCount.status_code == 200 and len(EmployerCount.json) > 1

def test_invalidJobOffer(client):
    data1 = {
        "email": "bigJoeDu91@cegeprdl.ca",
        "password": "test123"
    }
    response1 = client.post('/user/login', json=data1)
    token = response1.json['token']

    #Très gros titre (Plus grand que 255)
    job_offer1_data2 = {
        "id": 1,
        "title": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "address": "123 rue de la rue",
        "description": "Développeur fullstack",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2121-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": 40,
        "offerLink": "www.google.com",
        "salary": "1000",
        "offerDebut": "2021-12-12",
        "active": True,
        "approbationMessage": "Super offre!",
        "employerId": None,
        "isApproved": True,
        "approvedDate": datetime.now()
    }

    data2 = {
            "jobOffer": 
            job_offer1_data2,
            "enterprise": 
            {
                "id": 2,
                "name": "Google",
                "email": "google@gmail.com",
                "phone": "1234567890",
                "address": "123 rue google",
                "cityId": 1
            },
            "studyPrograms": [
                1,
                2
            ],
            "scheduleIds": [
                1
            ]
        }

    response2 = client.post('/jobOffer/new', json=data2, headers={'Authorization': token})

    assert response2.status_code == 400



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
    response = client.put(f'/jobOffer/approve/1', json=data, headers={'Authorization': token})
    assert response.status_code == 204

def test_updateJobOffer(client):
    data = {
        "jobOffer": {
        "id": 2,
        "title": "Développeur Fullstack",
        "address": "123 rue de la liberte",
        "description": "Développeur fullstack",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2021-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": 40,
        "offerLink": "www.google.com",
        "salary": '1000',
        "offerDebut": "2021-12-12",
        "active": True,
        "approbationMessage": "Super offre!",
        "employerId": 1,
        "isApproved": True
        },
        "studyPrograms": [5, 6] ,
        "scheduleIds": [1, 2]
    }

    data1 = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    responseLogin = client.post('/user/login', json=data1)
    token = responseLogin.json['token']
    response = client.put(f'/jobOffer/1', json=data, headers={'Authorization': token})
    assert response.status_code == 200
    assert VerifyData(response.json)