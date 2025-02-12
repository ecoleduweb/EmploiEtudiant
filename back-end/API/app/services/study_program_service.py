from app.repositories.study_program_repo import StudyProgramRepo
from app.customexception.CustomException import NotFoundException
study_program_repo = StudyProgramRepo()

class StudyProgramService:
    def studyPrograms(self):
        return study_program_repo.studyPrograms()

    def findById(self, id):
        return study_program_repo.findById(id)

    def editStudyProgram(self, id, name):
        if study_program_repo.studyProgramExist(id):
            return study_program_repo.editStudyProgram(id, name)            
        raise NotFoundException("Job not found")

    def addStudyProgram(self, name):
        if not study_program_repo.doesAlreadyExist(name):
            return study_program_repo.addStudyProgram(name)
        raise Exception("Already created")