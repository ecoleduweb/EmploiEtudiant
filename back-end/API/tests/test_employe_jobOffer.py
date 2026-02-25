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
    with app.test_client() as client:
        dataLogin = {
            "email": "test@gmail.com",
            "password": "test123"
        }
        res = client.post('/user/login', json=dataLogin)
        assert res.status_code == 200
        yield client


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

        enterprise_data2 = {
            "id": 2,
            "name": "Développeur",
            "email": "entreprise2@test.com",
            "phone": "321-321-4321",
            "address": "123 rue de la rue",
            "isTemporary": False,
            "cityId": 1,
        }
        enterprise = Enterprise(**enterprise_data)
        enterprise2 = Enterprise(**enterprise_data2)
        db.session.add(enterprise)
        db.session.add(enterprise2)
        employer_data = {
            "id": 1,
            "verified": True,
            "userId": 1,
            "enterpriseId": 1,
        }

        employer2_data = {
            "id": 2,
            "verified": True,
            "userId": 2,
            "enterpriseId": 1,
        }

        employer3_data = {
            "id": 3,
            "verified": True,
            "userId": None,
            "enterpriseId": 2,
        }

        employers = Employers(**employer_data)
        db.session.add(employers)
        employers2 = Employers(**employer2_data)    
        db.session.add(employers2)
        employers3 = Employers(**employer3_data)
        db.session.add(employers3)
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
            "employerId": 1,
            "isApproved": False
        }

        job_offer3_data = {
            "id": 3,
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
            "employerId": 3,
            "isApproved": False
        }
        job_offer2 = JobOffer(**job_offer2_data)
        job_offer3 = JobOffer(**job_offer3_data)
        db.session.add(job_offer2)
        db.session.add(job_offer3)
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
    response = client.get('/jobOffer/approved')
    assert response.status_code == 200
    assert len(response.json) == 1

def test_offresEmploiApprouveesWithDetails(client):
   
    response = client.get('/jobOffer/approved?entrepriseDetails=true&employmentScheduleDetails=true&studyProgramDetails=true')
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
    response = client.post('/jobOffer/new', json=data)
    assert response.status_code == 201



def test_CreateJobOffer_InvalidTitle(client):
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

    response2 = client.post('/jobOffer/new', json=data2)
    assert response2.get_json() == {'field': 'title', 'message': 'Ce champ doit comporter entre 1 et 255 caracteres.'}
    assert response2.status_code == 400

def test_CreateJobOffer_InvalidEmail(client):
    
    #Très gros titre (Plus grand que 255)
    job_offer1_data2 = {
        "id": 1,
        "title": "titre exemple",
        "address": "123 rue de la rue",
        "description": "Développeur fullstack",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2121-12-12",
        "email": "test@",
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

    response2 = client.post('/jobOffer/new', json=data2)
    assert response2.get_json() == {'field': 'email', 'message': 'Le format du courriel est invalide.'}
    assert response2.status_code == 400

def test_CreateJobOffer_InvalidNumber(client):

    #Très gros titre (Plus grand que 255)
    job_offer1_data2 = {
        "id": 1,
        "title": "titre exemple",
        "address": "123 rue de la rue",
        "description": "Développeur fullstack",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2121-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": "pasUnNombre",
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

    response2 = client.post('/jobOffer/new', json=data2)
    assert response2.get_json() == {'field': 'hoursPerWeek', 'message': 'Ce champ doit correspondre a un nombre.'}
    assert response2.status_code == 400


def test_updateJobOffer_InvalidTitle(client):
    data = {
        "jobOffer": {
        "id": 2,
        "title": "Développeur FullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstackFullstack",
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

    response = client.put(f'/jobOffer/1', json=data)
    assert response.get_json() == {'field': 'title', 'message': 'Ce champ doit comporter entre 1 et 255 caracteres.'}
    assert response.status_code == 400

def test_updateJobOffer_InvalidEmail(client):
    data = {
        "jobOffer": {
        "id": 2,
        "title": "Titre test",
        "address": "123 rue de la liberte",
        "description": "Développeur fullstack",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2021-12-12",
        "email": "test@",
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
    response = client.put(f'/jobOffer/1', json=data)
    assert response.get_json() == {'field': 'email', 'message': 'Le format du courriel est invalide.'}
    assert response.status_code == 400

def test_updateJobOffer_InvalidNumber(client):
    data = {
        "jobOffer": {
        "id": 2,
        "title": "Titre test",
        "address": "123 rue de la liberte",
        "description": "Développeur fullstack",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2021-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": "pasUnNombre",
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
    response = client.put(f'/jobOffer/1', json=data)
    assert response.get_json() == {'field': 'hoursPerWeek', 'message': 'Ce champ doit correspondre a un nombre.'}
    assert response.status_code == 400

def test_updateJobOffer_NotFound(client):
    data = {
        "jobOffer": {
        "id": 9,
        "title": "Titre test",
        "address": "123 rue de la liberte",
        "description": "Développeur fullstack",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2021-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": "40",
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
    response = client.put(f'/jobOffer/9', json=data)
    assert response.get_json() == {'message': 'Job offer not found.'}
    assert response.status_code == 404

def test_updateJobOffer_IsApproved(client):
    data = {
        "jobOffer": {
        "id": 2,
        "title": "Développeur Fullstack",
        "address": "123 rue de la liberte changé",
        "description": "Développeur fullstack",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2021-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": "40",
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

    response = client.put(f'/jobOffer/2', json=data)
    assert response.json['isApproved']==None
    assert response.status_code == 200
   



def test_updateJobOffer_IsApproved_ApprovedToNone(client):
    data = {
        "jobOffer": {
        "id": 2,
        "title": "Titre test changé",
        "address": "123 rue de la liberte",
        "description": "Développeur fullstack",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2021-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": "40",
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

    response = client.put(f'/jobOffer/2', json=data)
    assert response.json['isApproved'] == None
    assert response.status_code == 200

def test_updateJobOffer_IsApproved_DeclinedToNone(client):
    data = {
        "jobOffer": {
        "id": 2,
        "title": "Titre test",
        "address": "123 rue de la liberte changé",
        "description": "Développeur fullstack",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2021-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": "40",
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

    response = client.put(f'/jobOffer/2', json=data)
    assert response.json['isApproved'] == None
    assert response.status_code == 200

def test_updateJobOffer_OtherEntrepriseOffer(client):
    data = {
        "jobOffer": {
        "id": 2,
        "title": "Titre test changé",
        "address": "123 rue de la liberte",
        "description": "Développeur fullstack",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2021-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": "40",
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

    response = client.put(f'/jobOffer/3', json=data)
    assert response.status_code == 403
    assert response.json['message'] == 'Permission denied' 

def test_createJobOfferWithoutOfferLink(client):
   
    #Très gros titre (Plus grand que 255)
    job_offer1_data2 = {
        "id": 1,
        "title": "offre test 2",
        "address": "123 rue de la rue",
        "description": "Développeur fullstack",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2121-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": 40,
        "offerLink": " ",
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

    response2 = client.post('/jobOffer/new', json=data2)

    assert response2.status_code == 201

   

def test_deleteOwnJobOfferAsEmployee(client):
    response2 = client.delete(f'/jobOffer/delete/2')

    assert response2.status_code == 200
    assert response2.json['message'] == 'Job offer deleted'  

def test_deleteOthersJobOfferAsEmployee(client):
    response2 = client.delete(f'/jobOffer/delete/3')
    
    assert response2.status_code == 403
    assert response2.json['message'] == 'Permission denied'






