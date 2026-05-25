
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr

from app.dtos.study_program_dto import StudyProgramReadDTO
from app.dtos.employement_schedule_dto import EmploymentScheduleReadDTO
from app.dtos.enterprise_dto import EnterpriseCreateDTO, EnterpriseReadDTO

class _JobOfferBase(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    address: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=3, max_length=100000)
    dateEntryOffice: date
    email: EmailStr
    hoursPerWeek: float = Field(gt=0)
    offerLink: str = Field(max_length=255)
    salary: str = Field(max_length=255)
    offerDebut: date
    approbationMessage: str | None = Field(max_length=6000, default=None)
    enterpriseId: int
    isApproved: bool | None = False
    approvedDate: datetime | None = None
    last_modified_by_id: int | None = None
    lastModifiedDate: datetime | None = None
    deadlineApply: date
 
class JobOfferCreateDTO(_JobOfferBase):
    deadlineApply: date
    offerDebut: date
    dateEntryOffice: date
    studyPrograms: list[StudyProgramReadDTO] = []
    employmentSchedules: list[EmploymentScheduleReadDTO] = []
    enterprise: EnterpriseCreateDTO | None
    enterpriseId: int | None

class JobOfferUpdateDTO(_JobOfferBase):
    id: int
    studyPrograms: list[StudyProgramReadDTO] = []
    employmentSchedules: list[EmploymentScheduleReadDTO] = []

class JobOfferReadDTO(_JobOfferBase):
    id: int
    enterprise: EnterpriseReadDTO | None
    studyPrograms: list[StudyProgramReadDTO] = []
    employmentSchedules: list[EmploymentScheduleReadDTO] = []
    # Permet de convertir un objet SQLAlchemy en DTO en utilisant les attributs de l'objet au lieu des clés du dictionnaire.
    model_config = ConfigDict(from_attributes=True) 

class JobOfferApproveDTO(BaseModel):
    id: int | None = None
    selectedEnterpriseId: int
    approbationMessage: str = Field(max_length=6000)
    isApproved: bool

class DetailedJobOfferReadDTO(_JobOfferBase):
    id: int

    # Permet de convertir un objet SQLAlchemy en DTO en utilisant les attributs de l'objet au lieu des clés du dictionnaire.
    model_config = ConfigDict(from_attributes=True) 