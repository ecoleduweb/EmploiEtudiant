from app import db
from app.models.employment_schedule_model import EmploymentSchedule
from app.dtos.employement_schedule_dto import EmploymentScheduleReadDTO

class EmploymentScheduleRepo:
    def all(self):
        employmentSchedules = EmploymentSchedule.query.all()
        dtos = [EmploymentScheduleReadDTO.model_validate(e) for e in employmentSchedules]
        return dtos