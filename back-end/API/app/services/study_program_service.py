from app.repositories.study_program_repo import StudyProgramRepo
from app.customexception.exception import DuplicateException, NotFoundException

from app.dtos.study_program_dto import (
    StudyProgramCreateDTO,
    StudyProgramUpdateDTO,
    StudyProgramReadDTO,
)

study_program_repo = StudyProgramRepo()
class StudyProgramService:
    def find_all(self) -> list[StudyProgramReadDTO]:
        return study_program_repo.studyPrograms()

    def find_by_id(self, id) -> StudyProgramReadDTO:
        return study_program_repo.findById(id)

    def update(self, dto: StudyProgramUpdateDTO) -> StudyProgramReadDTO:
        return study_program_repo.update(dto)

    def add(self, dto: StudyProgramCreateDTO) -> StudyProgramReadDTO:
        if not study_program_repo.name_exists(dto):
            return study_program_repo.add(dto)
        raise DuplicateException("Name", "Study program with this name already exists")