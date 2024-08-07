from flask import jsonify, request, Blueprint
from app.services.employmentSchedule_service import EmploymentScheduleService
from app.middleware.tokenVerify import token_required
employment_schedule_service = EmploymentScheduleService()

employment_schedule_blueprint = Blueprint('employmentSchedule', __name__)

@employment_schedule_blueprint.route('/<int:id>', methods=['GET'])
@token_required
def employmentSchedule(current_user, id):
    employmentSchedule = employment_schedule_service.employmentSchedule(id)
    return employmentSchedule.to_json_string()

@employment_schedule_blueprint.route('/all', methods=['GET'])
@token_required
def employmentSchedules(current_user):
    employmentSchedules = employment_schedule_service.employmentSchedules()
    return [employmentSchedule.to_json_string() for employmentSchedule in employmentSchedules]

@employment_schedule_blueprint.route('/getByOfferId/<int:jobOfferId>', methods=['GET'])
def getScheduleFromJobOffer(jobOfferId):
    schedules = employment_schedule_service.getScheduleFromJobOffer(jobOfferId)
    return [schedule.to_json_string() for schedule in schedules]
