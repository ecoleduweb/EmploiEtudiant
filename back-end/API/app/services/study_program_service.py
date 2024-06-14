from app.repositories.study_program_repo import StudyProgramRepo
study_program_repo = StudyProgramRepo()

class StudyProgramService:
    def studyPrograms(self):
        return study_program_repo.studyPrograms()

    def findById(self, id):
        return study_program_repo.findById(id)

    def editStudyProgram(self, id, name):
        if jobOffer_repo.jobOfferExist(id):
            return study_program_repo.editStudyProgram(id, name)
        raise NotFoundException("Job not found")

    def addStudyProgram(self, name):
        return study_program_repo.addStudyProgram(name)