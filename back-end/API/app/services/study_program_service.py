from app.repositories.study_program_repo import StudyProgramRepo
study_program_repo = StudyProgramRepo()

class StudyProgramService:
    def studyPrograms(self):
        return study_program_repo.studyPrograms()
    
    def studyProgramId(self, name):
        return study_program_repo.studyProgramId(name)
    
    def addStudyProgram(self, name):
        return study_program_repo.addStudyProgram(name)