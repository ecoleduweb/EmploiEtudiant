from pydantic import BaseModel, ConfigDict, Field

class StudyProgramBase(BaseModel):
    name: str = Field(min_length=3, max_length=255)

class StudyProgramCreateDTO(StudyProgramBase):
    pass

class StudyProgramUpdateDTO(StudyProgramBase):
    id: int

class StudyProgramReadDTO(StudyProgramBase):
    id: int

    # Permet de convertir un objet SQLAlchemy en DTO en utilisant les attributs de l'objet au lieu des clés du dictionnaire.
    model_config = ConfigDict(from_attributes=True) 