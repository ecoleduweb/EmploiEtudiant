import sys
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from flask_cors import CORS
from flask import Flask, jsonify

from flask_swagger_ui import get_swaggerui_blueprint
from logging.config import dictConfig
from logging import getLogger
from argon2 import PasswordHasher


hasher = PasswordHasher()


dictConfig({
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        },
        "simpleformatter": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        },
    },
    "handlers": {
        "wsgi": {"class": "logging.StreamHandler", "formatter": "default"},
        "custom_handler": {
            "class": "logging.FileHandler",
            "formatter": "simpleformatter",
            "filename": "logs.txt",
            "level": "WARN",
        },
    },
    "root": {"level": "INFO", "handlers": ["wsgi", "custom_handler"]},
}
)
SWAGGER_URL_PREFIX = "/swagger"
SWAGGER_LOCATION = "/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL_PREFIX,
    SWAGGER_LOCATION,
    config={"app_name": "Gestion de demandes d'emplois"},
)


db = SQLAlchemy()

load_dotenv()

logger = getLogger(__name__)

def create_app():
    app = Flask(__name__)
    # Temporary CORS bypass
    CORS(app)
    # Set CORS origins
    CORS(app, origins=[os.environ.get('CORS')])

    try:
        # port 5001 is used for playwright tests
        if any("pytest" in arg for arg in sys.argv) or any("5001" in arg for arg in sys.argv):
            app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_TEST_URL')
            app.config['TESTING'] = True
            print("Running tests")
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_DEV_URL')
    except Exception as e:
        logger.warning("Error loading environment variables : " + str(e))
        return jsonify({'message': 'Error loading environment variables'}), 500

    db.init_app(app)

    #Do not remove.
    migrate = Migrate(app, db)
    # END do not remove
    from app.controllers.user_controller import user_blueprint
    from app.controllers.jobOffer_controller import job_offer_blueprint
    from app.controllers.city_controller import city_blueprint
    from app.controllers.ping_controller import ping_blueprint
    from app.controllers.enterprise_controller import enterprise_blueprint
    from app.controllers.employer_controller import employer_blueprint
    from app.controllers.study_program_controller import study_program_blueprint
    from app.controllers.offer_program_controller import offer_program_blueprint
    from app.controllers.employmentSchedule_controller import employment_schedule_blueprint
    
    app.register_blueprint(ping_blueprint)
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(job_offer_blueprint, url_prefix='/jobOffer')
    app.register_blueprint(enterprise_blueprint, url_prefix='/enterprise')
    app.register_blueprint(employer_blueprint, url_prefix='/employer')
    app.register_blueprint(city_blueprint, url_prefix='/city')
    app.register_blueprint(study_program_blueprint, url_prefix='/studyProgram')
    app.register_blueprint(offer_program_blueprint, url_prefix='/offerProgram')
    app.register_blueprint(employment_schedule_blueprint, url_prefix='/employmentSchedule')

    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL_PREFIX)
    

    with app.app_context(): 
        if any("5001" in arg for arg in sys.argv):
            from app.models.user_model import User 
            from app.models.city_model import City
            from app.models.region_model import Region
            from app.models.employmentSchedule_model import EmploymentSchedule
            print("Refreshing the database")
            db.drop_all()
            db.create_all()
            hashed_password = hasher.hash("test123")
            db.session.add(User(firstName="admin", lastName="admin", email="admin@gmail.com", password=hashed_password, active=True, isModerator=True))
            db.session.add(User(firstName="user", lastName="user", email="user@gmail.com", password=hashed_password, active=True, isModerator=False))
            db.session.add(Region(region="region"))
            db.session.add(City(city="ville", idRegion="1"))
            db.session.add(EmploymentSchedule(description="temps plein"))
            db.session.commit()
            print("database refreshed")

    return app
