import locale
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
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
import logging

hasher = PasswordHasher()

locale.setlocale(locale.LC_ALL, 'fr_FR.utf8') # Set locale to french (Permet de trier correctement avec les accents...)

dictConfig({
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
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
        if any("pytest" in arg for arg in sys.argv):
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

    resource = Resource(attributes={    
                ResourceAttributes.SERVICE_NAME: "EMPLOI_ETUDIANT_DEV",
                ResourceAttributes.SERVICE_VERSION: "1.0.0",
                ResourceAttributes.DEPLOYMENT_ENVIRONMENT: "development"
    })

    trace_provider = TracerProvider(resource=resource)
    otlp_trace_exporter = OTLPSpanExporter(endpoint="http://143.110.223.189:4318/v1/traces", timeout=5)
    trace_batch_processor = BatchSpanProcessor(otlp_trace_exporter)
    trace_provider.add_span_processor(trace_batch_processor)
    trace.set_tracer_provider(trace_provider)

    log_provider = LoggerProvider(resource=resource)
    otlp_log_exporter = OTLPLogExporter(endpoint="http://143.110.223.189:4318/v1/logs", timeout=5)
    batch_processor = BatchLogRecordProcessor(otlp_log_exporter)
    log_provider.add_log_record_processor(batch_processor)
    set_logger_provider(log_provider)


    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()

    with app.app_context():
        SQLAlchemyInstrumentor().instrument(engine=db.engine)

    LoggingInstrumentor().instrument(
        set_logging_format=True,
        log_level=logging.INFO,
        tracer_provider=trace_provider,
        logger_provider=log_provider,
    )

    @app.after_request
    def flush_telemetry(response):
        try:
            # Flush logs
            if batch_processor:
                batch_processor.force_flush()
            
            # Flush traces
            if trace_batch_processor:
                trace_batch_processor.force_flush()
            
            logger.debug("Telemetry flushed after request")
        except Exception as e:
            logger.error(f"Error flushing telemetry: {str(e)}")
        return response

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

    return app
