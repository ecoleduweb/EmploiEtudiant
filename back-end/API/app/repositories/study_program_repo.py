from app import locale
from app import db
from app.models.study_program_model import StudyProgram

class StudyProgramRepo:
    def studyPrograms(self):
        studyPrograms = StudyProgram.query.all()
        studyProgramsJson = [studyProgram.to_json_string() for studyProgram in studyPrograms]
        study_programs_sorted = sorted(studyProgramsJson, key=lambda e: locale.strxfrm(e['name']))
        return study_programs_sorted

    def findById(self, id):
        return StudyProgram.query.filter_by(id=id).first()

    def editStudyProgram(self, id, name):
        studyProgram = StudyProgram.query.filter_by(id=id).first()
        studyProgram.name = name
        db.session.commit()

    def addStudyProgram(self, name):
        new_study_program = StudyProgram(name=name)
        db.session.add(new_study_program)
        db.session.commit()
        return new_study_program

    def studyProgramExist(self, id):
        return StudyProgram.query.filter_by(id=id).first() is not None
    
    def doesAlreadyExist(self, name):
        return StudyProgram.query.filter_by(name=name).first() is not None