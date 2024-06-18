from app.repositories.employmentSchedule_repo import EmploymentScheduleRepo
employmentSchedule_repo = EmploymentScheduleRepo()

class EmploymentScheduleService:
    def employmentSchedules(self):
        return employmentSchedule_repo.employmentSchedules()
    
    def employmentSchedule(self, employmentScheduleId):
        return employmentSchedule_repo.employmentSchedule(employmentScheduleId)
    
    def linkOfferSchedule(self, scheduleIds, jobOfferId):
        return employmentSchedule_repo.linkOfferSchedule(scheduleIds, jobOfferId)
    
    def getScheduleFromJobOffer(self, jobOfferId):
        return employmentSchedule_repo.getScheduleFromJobOffer(jobOfferId)
    