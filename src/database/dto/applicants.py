from typing import Annotated

from pydantic import UUID4, Field

from database.dto.base import DTO
from database.dto.user import UserCreateDTO, UserEditDTO, UserDTO


class ApplicantDTO(DTO):
    id: Annotated[UUID4, Field(frozen=True)]
    user: UserDTO
    first_name: Annotated[str, Field(max_length=100)]
    middle_name: Annotated[str, Field(max_length=100)]
    last_name: Annotated[str, Field(max_length=100)]
    university: Annotated[str, Field(max_length=255)]
    graduation_year: int
    current_education_year: int
    about: Annotated[str, Field(max_length=255)]


class ApplicantCreateDTO(DTO):
    user: UserCreateDTO
    first_name: Annotated[str, Field(max_length=100)]
    middle_name: Annotated[str, Field(max_length=100)]
    last_name: Annotated[str, Field(max_length=100)]
    university: Annotated[str, Field(max_length=255)]
    graduation_year: int
    current_education_year: int
    about: Annotated[str | None, Field(max_length=255)] = None


class ApplicantEditDTO(DTO):
    user: UserEditDTO | None = None
    first_name: Annotated[str | None, Field(max_length=100)] = None
    middle_name: Annotated[str | None, Field(max_length=100)] = None
    last_name: Annotated[str | None, Field(max_length=100)] = None
    university: Annotated[str | None, Field(max_length=255)] = None
    graduation_year: int | None = None
    current_education_year: int | None = None
    about: Annotated[str | None, Field(max_length=255)] = None
