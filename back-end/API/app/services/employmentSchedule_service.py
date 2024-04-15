from app.repositories.employmentSchedule_repo import EmploymentScheduleRepo
employmentSchedule_repo = EmploymentScheduleRepo()

class EmploymentScheduleService:
    def employmentSchedules(self):
        return employmentSchedule_repo.employmentSchedules()
    
    def employmentSchedule(self, employmentScheduleId):
        return employmentSchedule_repo.employmentSchedule(employmentScheduleId)
    
    def employmentScheduleId(self, description):
        return employmentSchedule_repo.employmentScheduleId(description)