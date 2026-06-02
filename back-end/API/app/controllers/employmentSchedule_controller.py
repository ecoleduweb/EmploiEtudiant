from flask import jsonify, request, Blueprint
from app.services.employmentSchedule_service import EmploymentScheduleService
from app.middleware.tokenVerify import token_required
employment_schedule_service = EmploymentScheduleService()

employment_schedule_blueprint = Blueprint('employmentSchedule', __name__)


@employment_schedule_blueprint.route('/all', methods=['GET'])
def employmentSchedules():
    employmentSchedules = employment_schedule_service.get_all()
    return [es.model_dump() for es in employmentSchedules], 200
