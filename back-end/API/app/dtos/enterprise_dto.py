from app.dtos.city_dto import CityReadDTO
from pydantic import BaseModel, ConfigDict, Field, EmailStr

class _EterpriseBase(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    email: EmailStr = Field(max_length=255)
    phone: str = Field(min_length=3, max_length=255)
    address: str = Field(min_length=3, max_length=255)
    cityId: int

class EnterpriseCreateDTO(_EterpriseBase):
    isTemporary: bool = False
    pass

class EnterpriseUpdateDTO(_EterpriseBase):
    isTemporary: bool = False
    id: int

class EnterpriseReadDTO(_EterpriseBase):
    isTemporary: bool
    city: CityReadDTO
    id: int

    # Permet de convertir un objet SQLAlchemy en DTO en utilisant les attributs de l'objet au lieu des clés du dictionnaire.
    model_config = ConfigDict(from_attributes=True) 