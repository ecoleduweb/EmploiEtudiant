from pydantic import BaseModel, ConfigDict, Field

class _CityBase(BaseModel):
    city: str = Field(min_length=3, max_length=100)


class CityReadDTO(_CityBase):
    id: int
    idRegion: int
    # Permet de convertir un objet SQLAlchemy en DTO en utilisant les attributs de l'objet au lieu des clés du dictionnaire.
    model_config = ConfigDict(from_attributes=True) 