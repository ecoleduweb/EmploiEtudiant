from app.dtos.enterprise_dto import EnterpriseReadDTO
from pydantic import BaseModel, ConfigDict, Field, EmailStr

class _UserBase(BaseModel):
    firstName: str = Field(min_length=3, max_length=255)
    lastName: str = Field(min_length=3, max_length=255)
    email: EmailStr = Field(max_length=255)
    isModerator: bool  | None = None
    enterprise: EnterpriseReadDTO | None = None
    enterpriseId: int | None = None
    active: bool | None = None
    verified: bool | None = None

class UserLoginDTO(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(max_length=255)

class UserUpdatePasswordDTO(UserLoginDTO):
    password: str = Field(min_length=12, max_length=255)
    id: int | None = None

class UserLoginResponseDTO(_UserBase):
    password: str = Field(max_length=255)
    model_config = ConfigDict(from_attributes=True) 

class UserRegisterDTO(_UserBase):
    password: str = Field(min_length=12, max_length=255)
    captchaToken: str = Field(min_length=1)

class UserUpdateDTO(BaseModel):
    firstName: str = Field(min_length=3, max_length=255)
    lastName: str = Field(min_length=3, max_length=255)
    email: EmailStr = Field(max_length=255)
    id: int

class UserReadDTO(_UserBase):
    id: int
    # Permet de convertir un objet SQLAlchemy en DTO en utilisant les attributs de l'objet au lieu des clés du dictionnaire.
    password: str = Field(exclude=True)
    model_config = ConfigDict(from_attributes=True)  