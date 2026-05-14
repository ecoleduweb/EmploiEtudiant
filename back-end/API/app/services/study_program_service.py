from app.repositories.study_program_repo import StudyProgramRepo
from app.customexception.CustomException import DuplicateException, NotFoundException

from app.dtos.study_program_dto import (
    StudyProgramCreateDTO,
    StudyProgramUpdateDTO,
    StudyProgramReadDTO,
)

study_program_repo = StudyProgramRepo()
class StudyProgramService:
    def study_programs(self) -> list[StudyProgramReadDTO]:
        return study_program_repo.studyPrograms()

    def find_by_id(self, id) -> StudyProgramReadDTO:
        return study_program_repo.findById(id)

    def update(self, dto: StudyProgramUpdateDTO) -> StudyProgramReadDTO:
        if study_program_repo.id_exists(dto.id):
            return study_program_repo.update(dto)
        raise NotFoundException("Study program not found with id: " + str(dto.id))

    def add(self, dto: StudyProgramCreateDTO) -> StudyProgramReadDTO:
        if not study_program_repo.name_exists(dto):
            return study_program_repo.add(dto)
        raise DuplicateException("Name", "Study program with this name already exists")