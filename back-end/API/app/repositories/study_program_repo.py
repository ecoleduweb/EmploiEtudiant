from app import db
from app.models.study_program_model import StudyProgram

class StudyProgramRepo:
    def studyPrograms(self):
        studyPrograms = StudyProgram.query.all()
        return studyPrograms
    
    def studyProgramId(self, name):
        studyProgram = StudyProgram.query.filter_by(name=name).first()
        studyProgramId = studyProgram.id
        return studyProgramId

    def addStudyProgram(self, name):
        new_study_program = StudyProgram(name=name)
        db.session.add(new_study_program)
        db.session.commit()
        return new_study_program