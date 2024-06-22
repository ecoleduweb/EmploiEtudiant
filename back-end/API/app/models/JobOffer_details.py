class JobOfferDetails:
    def __init__(self, jobOffer, enterprise=None, employmentSchedules=None, studyPrograms=None):
        self.jobOffer = {
            'id': jobOffer.id,
            'title': jobOffer.title,
            'address': jobOffer.address,
            'description': jobOffer.description,
            'offerDebut': str(jobOffer.offerDebut),
            'dateEntryOffice': str(jobOffer.dateEntryOffice),
            'deadlineApply': str(jobOffer.deadlineApply),
            'email': jobOffer.email,
            'hoursPerWeek': jobOffer.hoursPerWeek,
            'offerLink': jobOffer.offerLink,
            'salary': jobOffer.salary,
            'active': jobOffer.active,
            'approbationMessage': jobOffer.approbationMessage,
            'employerId': jobOffer.employerId,
            'isApproved': jobOffer.isApproved,
            'approvedDate': str(jobOffer.approvedDate)  # Assurez-vous de convertir en chaîne si nécessaire
        }
        self.enterprise = enterprise if enterprise else {}
        self.employmentSchedules = employmentSchedules if employmentSchedules else {}
        self.studyPrograms = studyPrograms if studyPrograms else {}

    def setEnterprise(self, enterprise):
        self.enterprise = {
            'id': enterprise.id,
            'name': enterprise.name,
            'email': enterprise.email,
            'phone': enterprise.phone,
            'address': enterprise.address,
            'cityId': enterprise.cityId,
            'isTemporary': enterprise.isTemporary 
        }

    def setStudyPrograms(self, studyPrograms):
        self.studyPrograms = [{
            "id": studyProgram.id,
            "name": studyProgram.name
        } for studyProgram in studyPrograms]

    def setEmploymentSchedules(self, employmentSchedules):
        self.employmentSchedules = [{
            "id": employmentSchedule.id,
            "description": employmentSchedule.description
        } for employmentSchedule in employmentSchedules]

    def to_json_string(self):
        return {
            'jobOffer': self.jobOffer,
            'enterprise': self.enterprise,
            'employmentSchedules': self.employmentSchedules,
            'studyPrograms': self.studyPrograms
        }