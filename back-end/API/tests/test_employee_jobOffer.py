import pytest
from app import create_app, db
from app.models.job_offer_model import JobOffer
from app.models.user_model import User
from app.models.enterprise_model import Enterprise
from app.models.study_program_model import StudyProgram
from app.models.employment_schedule_model import EmploymentSchedule
from app.models.city_model import City
from app.models.region_model import Region
from datetime import datetime
from freezegun import freeze_time


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
    "offerDebut": "2020-12-12",
    "approbationMessage": "Super offre!",
    "enterpriseId": 1,
    "isApproved": True,
    "approvedDate": datetime.now(),
    "last_modified_by_id": 1
}

enterprise = Enterprise(**{
            "id": 1,
            "name": "Développeur",
            "email": "test@test.com",
            "phone": "123-123-1234",
            "address": "123 rue de la",
            "isTemporary": False,
            "cityId": 1,
        }
)
enterprise2 = Enterprise(**{
            "id": 2,
            "name": "Développeur",
            "email": "entreprise2@test.com",
            "phone": "321-321-4321",
            "address": "123 rue de la rue",
            "isTemporary": False,
            "cityId": 1,
        })
es =EmploymentSchedule(id=1, description="Temps plein")
sp1 = StudyProgram(id=1, name="Informatique")
sp2 = StudyProgram(id=2, name="Génie logiciel")


def VerifyData(jobOfferData):
    for data in job_offer1_data:
        if (data not in jobOfferData) and (type(jobOfferData[data]) != type(job_offer1_data[data])) :
            return False

    return True

@pytest.fixture(scope='module', autouse=True)
def freeze_test_date():
    with freeze_time("2021-11-15"):
        yield
        

@pytest.fixture(scope='module')
def client(app):
    with app.test_client() as client:
        dataLogin = {
            "email": "test@gmail.com",
            "password": "test123_12caracters!"
        }
        res = client.post('/auth/login', json=dataLogin)
        assert res.status_code == 200
        yield client


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

        
        db.session.add(enterprise)
        db.session.add(enterprise2)
        db.session.add(sp1)
        db.session.add(sp2)

        db.session.add(es)

        db.session.add(JobOffer(**{**job_offer1_data, "studyPrograms": [sp1, sp2], "employmentSchedules": [es]}))
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
            "offerDebut": "2020-12-12",
            "enterpriseId": 1,
            "isApproved": False,
            "studyPrograms": [sp1],
            "employmentSchedules": [es]
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
            "offerDebut": "2020-12-12",
            "enterpriseId": 2,
            "isApproved": False,
            "studyPrograms": [sp1],
            "employmentSchedules": [es]
        }
        job_offer2 = JobOffer(**job_offer2_data)
        job_offer3 = JobOffer(**job_offer3_data)
        db.session.add(job_offer2)
        db.session.add(job_offer3)

        hashed_password = hasher.hash("test123_12caracters!")
        user = User(id=1, firstName="Robert", lastName="Lizotte", email="test@gmail.com", password=hashed_password, active=True, isModerator=False, enterpriseId=1)
        db.session.add(user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


def test_getOfferById(client):
    response = client.get('/jobOffer/1')
    assert response.status_code == 200
    assert VerifyData(response.json)

def test_getallEmployerOffer(client):
    response = client.get('/jobOffer/employer/all')
    assert response.status_code == 200
    assert len(response.json) == 2

def test_offresEmploiApprouvees(client):
    response = client.get('/jobOffer/approved')
    assert response.status_code == 200
    assert len(response.json) == 1

def test_offresEmploiApprouveesWithDetails(client):
    response = client.get('/jobOffer/approved?entrepriseDetails=true&employmentScheduleDetails=true&studyProgramDetails=true')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['enterprise'] is not None
    assert len(response.json[0]['employmentSchedules']) == 1
    assert len(response.json[0]['studyPrograms']) == 2

def test_userCreateOffresEmploi(client):
    data = {
        "title": "Tout change",
        "address": "Tout change",
        "description": "Tout change",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2022-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": 40,
        "offerLink": "www.google.com",
        "salary": "1000",
        "offerDebut": "2021-12-12",
        "approbationMessage": "Super offre!",
        "enterpriseId": 1,
        "last_modified_by_id": 1,
        "studyPrograms": [{ "id": sp1.id, "name": sp1.name }, { "id": 2, "name": sp2.name }],
        "employmentSchedules": [{ "id": es.id, "description": es.description }],
        "enterprise": {
            "name": "Google",
            "email": "google@gmail.com",
            "phone": "1234567890",
            "address": "123 rue google",
            "cityId": 1
        },
    }
    response = client.post('/jobOffer/new', json=data)
    assert response.status_code == 201



def test_CreateJobOffer_InvalidTitle(client):
    data = {
        #Très gros titre (Plus grand que 255)
        "title": "*"*256,
        "address": "Tout change",
        "description": "Tout change",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2022-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": 40,
        "offerLink": "www.google.com",
        "salary": "1000",
        "offerDebut": "2021-12-12",
        "approbationMessage": "Super offre!",
        "enterpriseId": 1,
        "last_modified_by_id": 1,
        "studyPrograms": [{ "id": sp1.id, "name": sp1.name }, { "id": 2, "name": sp2.name }],
        "employmentSchedules": [{ "id": es.id, "description": es.description }],
        "enterprise": {
            "name": "Google",
            "email": "google@gmail.com",
            "phone": "1234567890",
            "address": "123 rue google",
            "cityId": 1
        },
    }
    response = client.post('/jobOffer/new', json=data)
    assert response.get_json()[0]['message'] == "s'assurer que cette valeur comporte au maximum 255 caractères"
    assert response.get_json()[0]['field'] == "title"
    assert response.status_code == 400

def test_CreateJobOffer_InvalidEmail(client):
    data = {
        #Très gros titre (Plus grand que 255)
        "title": "SUper offre!",
        "address": "Tout change",
        "description": "Tout change",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2022-12-12",
        "email": "test",
        "hoursPerWeek": 40,
        "offerLink": "www.google.com",
        "salary": "1000",
        "offerDebut": "2021-12-12",
        "approbationMessage": "Super offre!",
        "enterpriseId": 1,
        "last_modified_by_id": 1,
        "studyPrograms": [{ "id": sp1.id, "name": sp1.name }, { "id": 2, "name": sp2.name }],
        "employmentSchedules": [{ "id": es.id, "description": es.description }],
        "enterprise": {
            "name": "Google",
            "email": "google@gmail.com",
            "phone": "1234567890",
            "address": "123 rue google",
            "cityId": 1
        },
    }
    response = client.post('/jobOffer/new', json=data)
    assert response.get_json()[0]['message'] == "la valeur n'est pas valide"
    assert response.get_json()[0]['field'] == "email"
    assert response.status_code == 400

def test_CreateJobOffer_InvalidNumber(client):
    data = {
        "title": "SUper offre!",
        "address": "Tout change",
        "description": "Tout change",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2022-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": -1,
        "offerLink": "www.google.com",
        "salary": "1000",
        "offerDebut": "2021-12-12",
        "approbationMessage": "Super offre!",
        "enterpriseId": 1,
        "last_modified_by_id": 1,
        "studyPrograms": [{ "id": sp1.id, "name": sp1.name }, { "id": 2, "name": sp2.name }],
        "employmentSchedules": [{ "id": es.id, "description": es.description }],
        "enterprise": {
            "name": "Google",
            "email": "google@gmail.com",
            "phone": "1234567890",
            "address": "123 rue google",
            "cityId": 1
        },
    }
    response = client.post('/jobOffer/new', json=data)
    assert response.get_json()[0]['message'] == "s'assurer que cette valeur est supérieure à 0.0"
    assert response.get_json()[0]['field'] == "hoursPerWeek"
    assert response.status_code == 400

def test_updateJobOffer_NotFound(client):
    data = {
        "id": 9,
        "title": "SUper offre!",
        "address": "Tout change",
        "description": "Tout change",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2022-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": 10,
        "offerLink": "www.google.com",
        "salary": "1000",
        "offerDebut": "2021-12-12",
        "approbationMessage": "Super offre!",
        "enterpriseId": 1,
        "last_modified_by_id": 1,
        "studyPrograms": [{ "id": sp1.id, "name": sp1.name }, { "id": 2, "name": sp2.name }],
        "employmentSchedules": [{ "id": es.id, "description": es.description }],
        "enterprise": {
            "name": "Google",
            "email": "google@gmail.com",
            "phone": "1234567890",
            "address": "123 rue google",
            "cityId": 1
        },
    }
    response = client.put(f'/jobOffer/9', json=data)
    assert response.status_code == 404

def test_updateJobOffer_IsApprovedToNone(client):
    data = {
        "id": 2,
        "title": "SUper offre!",
        "address": "Tout change",
        "description": "Tout change",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2022-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": 10,
        "offerLink": "www.google.com",
        "salary": "1000",
        "offerDebut": "2021-12-12",
        "approbationMessage": "Super offre!",
        "enterpriseId": 1,
        "IsApproved": True,
        "last_modified_by_id": 1,
        "studyPrograms": [{ "id": sp1.id, "name": sp1.name }, { "id": 2, "name": sp2.name }],
        "employmentSchedules": [{ "id": es.id, "description": es.description }],
        "enterprise": {
            "name": "Google",
            "email": "google@gmail.com",
            "phone": "1234567890",
            "address": "123 rue google",
            "cityId": 1
        },
    }

    response = client.put(f'/jobOffer/2', json=data)
    assert response.json['isApproved']==None
    assert response.status_code == 200


def test_updateJobOffer_IsApproved_ApprovedFalseToNone(client):
    data = {
        "id": 2,
        "title": "SUper offre!",
        "address": "Tout change",
        "description": "Tout change",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2022-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": 10,
        "offerLink": "www.google.com",
        "salary": "1000",
        "offerDebut": "2021-12-12",
        "approbationMessage": "Super offre!",
        "enterpriseId": 1,
        "IsApproved": True,
        "last_modified_by_id": 1,
        "studyPrograms": [{ "id": sp1.id, "name": sp1.name }, { "id": 2, "name": sp2.name }],
        "employmentSchedules": [{ "id": es.id, "description": es.description }],
        "enterprise": {
            "name": "Google",
            "email": "google@gmail.com",
            "phone": "1234567890",
            "address": "123 rue google",
            "cityId": 1
        },
    }

    response = client.put(f'/jobOffer/2', json=data)
    assert response.status_code == 200
    assert response.json['isApproved'] is None


def test_updateJobOffer_OtherEntrepriseOffer(client):
    data = {
        "id": 3,
        "title": "SUper offre!",
        "address": "Tout change",
        "description": "Tout change",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2022-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": 10,
        "offerLink": "www.google.com",
        "salary": "1000",
        "offerDebut": "2021-12-12",
        "approbationMessage": "Super offre!",
        "enterpriseId": 1,  # Essaie de changer l'entreprise pour la sienne
        "IsApproved": True,
        "last_modified_by_id": 1,
        "studyPrograms": [{ "id": sp1.id, "name": sp1.name }, { "id": 2, "name": sp2.name }],
        "employmentSchedules": [{ "id": es.id, "description": es.description }],
        "enterprise": {
            "name": "Google",
            "email": "google@gmail.com",
            "phone": "1234567890",
            "address": "123 rue google",
            "cityId": 1
        },
    }

    response = client.put(f'/jobOffer/3', json=data)
    assert response.status_code == 403

def test_createJobOfferWithoutOfferLink(client):
   data = {
        "id": 3,
        "title": "SUper offre!",
        "address": "Tout change",
        "description": "Tout change",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2022-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": 10,
        "salary": "1000",
        "offerLink": '',
        "offerDebut": "2021-12-12",
        "approbationMessage": "Super offre!",
        "enterpriseId": 1,  # Essaie de changer l'entreprise pour la sienne
        "IsApproved": True,
        "last_modified_by_id": 1,
        "studyPrograms": [{ "id": sp1.id, "name": sp1.name }, { "id": 2, "name": sp2.name }],
        "employmentSchedules": [{ "id": es.id, "description": es.description }],
        "enterprise": {
            "name": "Google",
            "email": "google@gmail.com",
            "phone": "1234567890",
            "address": "123 rue google",
            "cityId": 1
        },
    }
   response = client.post('/jobOffer/new', json=data)
   assert response.status_code == 201

def test_deleteOwnJobOfferAsEmployee(client):
    response2 = client.delete(f'/jobOffer/2')
    assert response2.status_code == 204

def test_deleteOthersJobOfferAsEmployee(client):
    response2 = client.delete(f'/jobOffer/3')
    assert response2.status_code == 403
