from app.repositories.employmentSchedule_repo import EmploymentScheduleRepo
from app.dtos.employement_schedule_dto import EmploymentScheduleReadDTO
employmentSchedule_repo = EmploymentScheduleRepo()

class EmploymentScheduleService:
    def get_all(self) -> list[EmploymentScheduleReadDTO]:
        return employmentSchedule_repo.all()
    