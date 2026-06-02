from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from app.dtos.city_dto import CityReadDTO  # not part of the cycle — leave at top

if TYPE_CHECKING:
    from app.dtos.user_dto import UserReadDTO


class _EnterpriseBase(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    email: str
    phone: str = Field(max_length=255)
    address: str = Field(min_length=3, max_length=255)
    cityId: int


class EnterpriseCreateDTO(_EnterpriseBase):
    isTemporary: bool = False


class EnterpriseUpdateDTO(_EnterpriseBase):
    isTemporary: bool = False
    users: list[UserInEnterpriseDTO]
    id: int


class EnterpriseReadDTO(_EnterpriseBase):
    users: list[UserInEnterpriseDTO]
    isTemporary: bool
    city: CityReadDTO
    id: int

    # Convertit un objet SQLAlchemy en DTO via les attributs de l'objet.
    model_config = ConfigDict(from_attributes=True)


# Résout les forward refs une fois que UserReadDTO est importable.
from app.dtos.user_dto import UserInEnterpriseDTO  # noqa: E402

EnterpriseReadDTO.model_rebuild()