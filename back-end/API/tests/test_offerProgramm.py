import pytest
from app import create_app, db
from app.models.offer_programm_model import OfferProgram


@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

def test_linkOfferProgram(client):
    data = {
        "studyProgramId": 1,
        "offerId": 1
    }
    response = client.post('/offerProgram/linkOfferProgram', json=data)
    assert response.status_code == 200

