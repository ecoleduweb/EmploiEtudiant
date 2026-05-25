from pydantic import BaseModel, ConfigDict, Field

class _EmploymentScheduleBase(BaseModel):
    description: str = Field(min_length=3, max_length=255)

class EmploymentScheduleCreateDTO(_EmploymentScheduleBase):
    pass

class EmploymentScheduleUpdateDTO(_EmploymentScheduleBase):
    id: int

class EmploymentScheduleReadDTO(_EmploymentScheduleBase):
    id: int

    # Permet de convertir un objet SQLAlchemy en DTO en utilisant les attributs de l'objet au lieu des clés du dictionnaire.
    model_config = ConfigDict(from_attributes=True) 