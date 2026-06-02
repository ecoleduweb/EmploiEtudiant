from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import Annotated
from pydantic import BaseModel, ConfigDict, Field, EmailStr, StringConstraints

if TYPE_CHECKING:
    from app.dtos.enterprise_dto import EnterpriseReadDTO


class _UserBase(BaseModel):
    firstName: str = Field(max_length=255)
    lastName: str = Field(max_length=255)
    email: Annotated[EmailStr, StringConstraints(max_length=255)]
    isModerator: bool | None = None
    enterprise: EnterpriseReadDTO | None = None
    enterpriseId: int | None = None
    verified: bool | None = None
    active: bool | None = None


class UserLoginDTO(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(max_length=255)


class UserUpdatePasswordDTO(BaseModel):
    password: str = Field(min_length=12, max_length=255)
    id: int | None = None


class UserLoginResponseDTO(_UserBase):
    id: int
    password: str = Field(max_length=255)
    isModerator: bool
    model_config = ConfigDict(from_attributes=True)


class UserRegisterDTO(_UserBase):
    password: str = Field(min_length=12, max_length=255)
    captchaToken: str = Field(min_length=1)


class UserUpdateDTO(BaseModel):
    id: int
    firstName: str = Field(min_length=3, max_length=255)
    lastName: str = Field(min_length=3, max_length=255)
    email: Annotated[EmailStr, StringConstraints(max_length=255)]


class UpdatedUserReadDTO(_UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserReadDTO(_UserBase):
    id: int
    password: str
    model_config = ConfigDict(from_attributes=True)

class UserInEnterpriseDTO(BaseModel):
    firstName: str = Field(min_length=3, max_length=255)
    lastName: str = Field(min_length=3, max_length=255)
    email: Annotated[EmailStr, StringConstraints(max_length=255)]
    isModerator: bool | None = None
    enterpriseId: int | None = None   # keep the FK so the client still knows which enterprise
    verified: bool | None = None
    active: bool | None = None
    id: int
    model_config = ConfigDict(from_attributes=True)


# Résout les forward refs une fois que EnterpriseReadDTO est importable.
from app.dtos.enterprise_dto import EnterpriseReadDTO  # noqa: E402

for _m in (UserLoginResponseDTO, UserRegisterDTO, UpdatedUserReadDTO, UserReadDTO):
    _m.model_rebuild()