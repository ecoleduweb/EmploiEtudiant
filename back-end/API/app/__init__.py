import sys
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import pymysql
from flask_cors import CORS

db = SQLAlchemy()

pymysql.install_as_MySQLdb()
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    CORS(app, origins='http://10.172.80.144, http://localhost')


    try:
        if any("pytest" in arg for arg in sys.argv):
            app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_TEST_URL')
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_DEV_URL')
            print("Running in development mode.")
    except Exception as e:
        print(e)
        print("Error loading environment variables.")
        return jsonify({'message': 'Error loading environment variables'}), 500
    
    db.init_app(app)

    from app.controllers.user_controller import app_blueprint
    app.register_blueprint(app_blueprint)

    return app