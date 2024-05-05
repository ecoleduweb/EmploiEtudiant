from flask import jsonify, request, Blueprint
from app.services.employmentSchedule_service import EmploymentScheduleService
from app.middleware.tokenVerify import token_required
employment_schedule_service = EmploymentScheduleService()

employment_schedule_blueprint = Blueprint('employmentSchedule', __name__)

@employment_schedule_blueprint.route('/employmentSchedule/<int:id>', methods=['GET'])
@token_required
def employmentSchedule(current_user):
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