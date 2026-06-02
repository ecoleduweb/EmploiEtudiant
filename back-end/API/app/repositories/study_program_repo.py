from app import locale
from app import db
from app.models.study_program_model import StudyProgram
from app.customexception.exception import NotFoundException

from app.dtos.study_program_dto import (
    StudyProgramReadDTO,
    StudyProgramCreateDTO,
    StudyProgramUpdateDTO
)
class StudyProgramRepo:
    def studyPrograms(self) -> list[StudyProgramReadDTO]:
        studyPrograms = StudyProgram.query.all()
        # Fix pas très élégant pour mettre "Tous les programmes" en premier
        study_programs_sorted = sorted(studyPrograms, key=lambda e: (0 if e.name == "Tous les programmes" else 1, locale.strxfrm(e.name)))
        dtos = [StudyProgramReadDTO.model_validate(sp) for sp in study_programs_sorted]
        return dtos

    def find_by_id(self, id) -> StudyProgramReadDTO:
        study_program = StudyProgram.query.filter_by(id=id).first()
        if study_program is None:
            raise NotFoundException(f"Study program not found with id: {id}")
        return StudyProgramReadDTO.model_validate(study_program)

    def update(self, dto: StudyProgramUpdateDTO) -> StudyProgramReadDTO:
        studyProgram = StudyProgram.query.filter_by(id=dto.id).first()
        if studyProgram is None:
            raise NotFoundException(f"Study program not found with id: {dto.id}")
        studyProgram.name = dto.name
        db.session.commit()
        return StudyProgramReadDTO.model_validate(studyProgram)

    def create(self, dto: StudyProgramCreateDTO) -> StudyProgramReadDTO:
        new_study_program = StudyProgram(**dto.model_dump())
        db.session.add(new_study_program)
        db.session.commit()
        return StudyProgramReadDTO.model_validate(new_study_program)

    def id_exists(self, id) -> bool:
        return StudyProgram.query.filter_by(id=id).first() is not None

    def name_exists(self, dto: StudyProgramCreateDTO) -> bool:
        return StudyProgram.query.filter_by(name=dto.name).first() is not None