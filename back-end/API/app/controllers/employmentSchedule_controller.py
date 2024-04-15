from flask import jsonify, request, Blueprint
import os
from app import db
from app.models.user_model import User
from jwt import decode
from functools import wraps
from app.models.region_model import Region
from app.controllers.user_controller import token_required
from app.services.employmentSchedule_service import EmploymentScheduleService
employment_schedule_service = EmploymentScheduleService()

employment_schedule_blueprint = Blueprint('employmentSchedule', __name__)


def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
            if not token:
                return jsonify({'message': 'a valid token is missing'})

            try:
                data = decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
                current_user = User.query.filter_by(email = data['email']).first()

            except Exception as e:
                print(e)
                return jsonify({'message': 'token is invalid'})
            return f(current_user)
        return decorated


@employment_schedule_blueprint.route('/employmentSchedule', methods=['GET'])
@token_required
def employmentSchedule():
    id = request.args.get('id')
    employmentSchedule = employment_schedule_service.employmentSchedule(id)
    return jsonify(employmentSchedule)

@employment_schedule_blueprint.route('/employmentSchedules', methods=['GET'])
@token_required
def employmentSchedules(current_user):
    employmentSchedules = employment_schedule_service.employmentSchedules()
    return [employmentSchedule.to_json_string() for employmentSchedule in employmentSchedules]

@employment_schedule_blueprint.route('/employmentScheduleId', methods=['POST'])
@token_required
def employmentScheduleId(current_user):
    description = request.args.get('description')
    employmentScheduleId = employment_schedule_service.employmentScheduleId(description)
    return jsonify(employmentScheduleId)