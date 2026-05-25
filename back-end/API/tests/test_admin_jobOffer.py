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
from argon2 import PasswordHasher
from freezegun import freeze_time

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
    "approbationMessage": "Super offre!",
    "enterpriseId": 1,
    "isApproved": True,
    "approvedDate": datetime.now(),
    "last_modified_by_id": 1
}

sp1 = StudyProgram(id=1, name="Informatique")
sp2 = StudyProgram(id=2, name="Génie logiciel")
es =EmploymentSchedule(id=1, description="Temps plein")

def VerifyData(jobOfferData):
    for data in job_offer1_data:
        if (data not in jobOfferData) and (type(jobOfferData[data]) != type(job_offer1_data[data])):
            return False
    return True

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

        db.session.add(Enterprise(
            id=1,
            name="Développeur",
            email="test@test.com",
            phone="123-123-1234",
            address="123 rue de la",
            isTemporary=False,
            cityId=1
        ))

        db.session.add(Enterprise(
            id=2,
            name="Entreprise 2",
            email="entreprise2@test.com",
            phone="321-321-4321",
            address="123 rue de la rue",
            isTemporary=True,
            cityId=1,
        ))

        db.session.add(Enterprise(
            id=3,
            name="Entreprise 3",
            email="entreprise3@test.com",
            phone="456-456-7890",
            address="456 rue de la rue",
            isTemporary=True,
            cityId=1,
        ))
        
        db.session.add(sp1)
        db.session.add(sp2)

        
        db.session.add(es)

        db.session.add(JobOffer(**{**job_offer1_data, "studyPrograms": [sp1, sp2], "employmentSchedules": [es]}))

        db.session.add(JobOffer(
            id=2,
            title="Développeur",
            address="123 rue de la rue",
            description="Développeur front-end",
            dateEntryOffice="2021-12-12",
            deadlineApply="2121-12-12",
            email="test@gmail.com",
            hoursPerWeek=40,
            offerLink="www.google.com",
            salary="1000",
            offerDebut="2021-12-12",
            enterpriseId=1,
            isApproved=False,
            studyPrograms=[sp1],
            employmentSchedules=[es]
        ))

        db.session.add(JobOffer(
            id=3,
            title="Développeur",
            address="123 rue de la rue",
            description="Développeur front-end",
            dateEntryOffice="2021-12-12",
            deadlineApply="2121-12-12",
            email="test@gmail.com",
            hoursPerWeek=40,
            offerLink="www.google.com",
            salary="1000",
            offerDebut="2021-12-12",
            enterpriseId=2,
            isApproved=None,
            studyPrograms=[sp1],
            employmentSchedules=[es],
            last_modified_by_id=1
        ))

        
        db.session.add(JobOffer(
            id=4,
            title="Développeur",
            address="123 rue de la rue",
            description="Développeur front-end",
            dateEntryOffice="2021-12-12",
            deadlineApply="2121-12-12",
            email="test@gmail.com",
            hoursPerWeek=40,
            offerLink="www.google.com",
            salary="1000",
            offerDebut="2021-12-12",
            enterpriseId=3,
            isApproved=None,
            studyPrograms=[sp1],
            employmentSchedules=[es],
            last_modified_by_id=2
        ))


        hashed_password = hasher.hash("test123_12caracters!")

        db.session.add(User(
            id=1,
            firstName="Robert",
            lastName="Lizotte",
            email="test@gmail.com",
            password=hashed_password,
            isModerator=False,
            enterpriseId=2
        ))

        db.session.add(User(
            id=2,
            firstName="Joe",
            lastName="Baril",
            email="bigJoeDu91@cegeprdl.ca",
            password=hashed_password,
            isModerator=False,
            enterpriseId=3
        ))

        db.session.add(User(
            id=3,
            firstName="admin",
            lastName="admin",
            email="admin@gmail.com",
            password=hashed_password,
            isModerator=True,
            active=True,
        ))

        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def client(app):
    with app.test_client() as client:
        client.post('/auth/login', json={
            "email": "admin@gmail.com",
            "password": "test123_12caracters!"
        })
        yield client


def test_adminCreateOffer(client):
    data = {
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


def test_updateJobOffer(client):
    data =  {
        "id": 2,
        "title": "Développeur Fullstack",
        "address": "123 rue de la liberte",
        "description": "Développeur fullstack",
        "dateEntryOffice": "2021-12-12",
        "deadlineApply": "2021-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": 40,
        "offerLink": "www.google.com",
        "salary": "1000",
        "offerDebut": "2021-12-12",
        "isApproved": True,
        "approbationMessage": "Super offre!",
        "enterpriseId": 1,
        "studyPrograms": [{ "id": 2, "name": sp2.name }],
        "employmentSchedules": [{ "id": es.id, "description": es.description }],
    }

    response = client.put('/jobOffer/1', json=data)
    assert response.status_code == 200
    assert VerifyData(response.json)


def test_updateJobOffer_IsApproved_IsAdmin(client):
    data = {
        "id": 2,
        "title": "Tout change",
        "address": "Tout change",
        "description": "Tout change",
        "dateEntryOffice": "2021-12-12", 
        "deadlineApply": "2021-12-12",
        "email": "test@gmail.com",
        "hoursPerWeek": 40,
        "offerLink": "www.google.com",
        "salary": "1000",
        "offerDebut": "2021-12-12",
        "isApproved": True,
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

    response = client.put('/jobOffer/2', json=data)
    assert response.status_code == 200
    assert response.json.get('isApproved') is True


def test_deleteJobOfferNotExist(client):
    response = client.delete('/jobOffer/15')
    assert response.status_code == 404
    assert response.json['message'] == 'Job offer not found'

def test_disapproveJobOfferAndAndValidatedEnterprise(client):
    response = client.put('/jobOffer/approve/3', json={'isApproved': False, 'approbationMessage': "", 'selectedEnterpriseId': 1})
    assert response.status_code == 200
    assert response.json.get('isApproved') is False
    response =  client.get('/enterprise/2')
    assert response.status_code == 200
    assert response.json.get('isTemporary') is True
    response =  client.get('/user/1')
    assert response.status_code == 200
    assert response.json.get('enterpriseId') == 2

def test_approveJobOfferAndDeleteEnterprise(client):
    response = client.put('/jobOffer/approve/3', json={'isApproved': True, 'approbationMessage': "", 'selectedEnterpriseId': 1})
    assert response.status_code == 200  
    assert response.json.get('isApproved') is True
    assert response.json.get('enterpriseId') == 1
    response =  client.get('/enterprise/2')
    assert response.status_code == 404
    response =  client.get('/user/1')
    assert response.status_code == 200
    assert response.json.get('enterpriseId') == 1


def test_approveJobOfferAndApproveEnterprise(client):
    response = client.put('/jobOffer/approve/4', json={'isApproved': True, 'approbationMessage': "", 'selectedEnterpriseId': 3})
    assert response.status_code == 200
    assert response.json.get('isApproved') is True
    response =  client.get('/enterprise/3')
    assert response.status_code == 200  
    assert response.json.get('isTemporary') is False
    response =  client.get('/user/2')
    assert response.status_code == 200
    assert response.json.get('enterpriseId') == 3

def test_deleteJobOfferAsAdmin(client):
    response = client.delete('/jobOffer/1')
    assert response.status_code == 200
    assert response.json['id'] == 1
    response = client.get('/jobOffer/1')
    assert response.status_code == 404