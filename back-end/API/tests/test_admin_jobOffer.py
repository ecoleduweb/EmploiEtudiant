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
        if data not in jobOfferData or not isinstance(jobOfferData[data], type(job_offer1_data[data])):
            return False
    return True


@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()

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
            isTemporary=False,
            cityId=1
        ))

        db.session.add(Employers(id=1, verified=True, userId=1, enterpriseId=1))
        db.session.add(Employers(id=2, verified=True, userId=2, enterpriseId=1))
        db.session.add(Employers(id=3, verified=True, userId=None, enterpriseId=2))

        db.session.add(JobOffer(**job_offer1_data))

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
            active=True,
            employerId=None,
            isApproved=False
        ))

        db.session.add(StudyProgram(id=1, name="Informatique"))
        db.session.add(StudyProgram(id=2, name="Génie logiciel"))

        db.session.add(EmploymentSchedule(id=1, description="Temps plein"))

        hashed_password = hasher.hash("test123")

        db.session.add(User(
            id=1,
            firstName="Robert",
            lastName="Lizotte",
            email="test@gmail.com",
            password=hashed_password,
            active=True,
            isModerator=False
        ))

        db.session.add(User(
            id=2,
            firstName="Joe",
            lastName="Baril",
            email="bigJoeDu91@cegeprdl.ca",
            password=hashed_password,
            active=True,
            isModerator=True
        ))

        db.session.add(User(
            id=3,
            firstName="admin",
            lastName="admin",
            email="admin@gmail.com",
            password=hashed_password,
            active=True,
            isModerator=True
        ))

        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def client(app):
    with app.test_client() as client:
        client.post('/user/login', json={
            "email": "admin@gmail.com",
            "password": "test123"
        })
        yield client


def test_adminCreateOffer(client):
    data = {
        "jobOffer": job_offer1_data,
        "enterprise": {
            "id": 1,
            "name": "Google",
            "email": "google@gmail.com",
            "phone": "1234567890",
            "address": "123 rue google",
            "cityId": 1
        },
        "studyPrograms": [1, 2],
        "scheduleIds": [1]
    }

    response = client.post('/jobOffer/new', json=data)
    assert response.status_code == 201


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
            "salary": "1000",
            "offerDebut": "2021-12-12",
            "active": True,
            "approbationMessage": "Super offre!",
            "employerId": 1,
            "isApproved": True
        },
        "studyPrograms": [1, 2],
        "scheduleIds": [1]
    }

    response = client.put('/jobOffer/1', json=data)
    assert response.status_code == 200
    assert VerifyData(response.json)


def test_updateJobOffer_IsApproved_IsAdmin(client):
    data = {
        "jobOffer": {
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
            "active": True,
            "approbationMessage": "Super offre!",
            "employerId": 1,
            "isApproved": True
        },
        "studyPrograms": [1, 2],
        "scheduleIds": [1]
    }

    response = client.put('/jobOffer/2', json=data)
    assert response.status_code == 200
    assert response.json.get('isApproved') is True


def test_deleteJobOfferNotExist(client):
    response = client.delete('/jobOffer/delete/15')
    assert response.status_code == 404
    assert response.json['message'] == 'Job offer not found'


def test_deleteJobOfferAsAdmin(client):
    response = client.delete('/jobOffer/delete/1')
    assert response.status_code == 200
    assert response.json['message'] == 'Job offer deleted'