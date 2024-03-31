import sys
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
import os
import pymysql
from flask_migrate import Migrate
from flask_cors import CORS
from flask import Flask, jsonify

from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL="/swagger"
API_URL="/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Gestion de demandes d'emplois"
    }
)


db = SQLAlchemy()

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Set CORS origins
    CORS(app, origins=[os.environ.get('CORS')])
    
    try:
        if any("pytest" in arg for arg in sys.argv):
            app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_TEST_URL')
            print("Running tests")
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_DEV_URL')
    except Exception as e:
        print(e)
        print("Error loading environment variables.")
        return jsonify({'message': 'Error loading environment variables'}), 500

    db.init_app(app)
    migrate = Migrate(app, db)
    
    from app.controllers.user_controller import user_blueprint
    from app.controllers.jobOffer_controller import job_offer_blueprint
    from app.controllers.city_controller import city_blueprint
    from app.controllers.enterprise_controller import enterprise_blueprint
    from app.controllers.employer_controller import employer_blueprint
    from app.controllers.study_program_controller import study_program_blueprint
    from app.controllers.offer_program_controller import offer_program_blueprint

    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(job_offer_blueprint, url_prefix='/jobOffer')
    app.register_blueprint(enterprise_blueprint, url_prefix='/enterprise')
    app.register_blueprint(employer_blueprint, url_prefix='/employer')
    app.register_blueprint(city_blueprint, url_prefix='/city')
    app.register_blueprint(study_program_blueprint, url_prefix='/studyProgram')
    app.register_blueprint(offer_program_blueprint, url_prefix='/offerProgram')

    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    


    return app
