from app.repositories.employmentSchedule_repo import EmploymentScheduleRepo
from app.repositories.jobOffer_repo import JobOfferRepo
from app.dtos.employement_schedule_dto import EmploymentScheduleReadDTO
employmentSchedule_repo = EmploymentScheduleRepo()
job_offer_repo = JobOfferRepo()

class EmploymentScheduleService:
    def get_all(self) -> list[EmploymentScheduleReadDTO]:
        return employmentSchedule_repo.all()
    