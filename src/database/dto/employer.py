from datetime import datetime
from typing import Annotated

from pydantic import UUID4, Field, field_serializer

from database.dto.base import DTO
from database.dto.user import UserCreateDTO, UserDTO, UserEditDTO


class EmployerDTO(DTO):
    id: Annotated[UUID4, Field(frozen=True)]
    user: UserDTO
    company_id: Annotated[UUID4, Field(frozen=True)]
    position: Annotated[str, Field(max_length=100)]
    created_at: Annotated[datetime, Field(frozen=True)]

    @field_serializer("created_at")
    def serialize_datetime(self, dt: datetime) -> str | None:
        if dt is None:
            return None
        return dt.strftime("%Y-%m-%d %H:%M")


class EmployerCreateDTO(DTO):
    user: UserCreateDTO
    company_id: Annotated[UUID4, Field(frozen=True)]
    position: Annotated[str, Field(max_length=100)]


class EmployerEditDTO(DTO):
    user: UserEditDTO | None = None
    company_id: Annotated[UUID4 | None, Field(frozen=True)] = None
    position: Annotated[str | None, Field(max_length=100)] = None
