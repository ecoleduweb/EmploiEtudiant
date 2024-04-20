from app import db
from app.models.study_program_model import StudyProgram

class StudyProgramRepo:
    def studyPrograms(self):
        studyPrograms = StudyProgram.query.all()
        studyProgramsJson = [studyProgram.to_json_string() for studyProgram in studyPrograms]
        return studyProgramsJson
    
    def studyProgramId(self, name):
        studyProgram = StudyProgram.query.filter_by(name=name).first()
        studyProgramId = studyProgram.id
        return studyProgramId

    def addStudyProgram(self, name):
        new_study_program = StudyProgram(name=name)
        db.session.add(new_study_program)
        db.session.commit()
        return new_study_program