from datetime import datetime
from typing import Annotated

from pydantic import UUID4, Field, field_serializer

from database.dto.base import DTO


class UserDTO(DTO):
    id: Annotated[UUID4, Field(frozen=True)]
    phone: Annotated[str, Field(max_length=20)]
    email: Annotated[str, Field(max_length=100)]
    display_name: Annotated[str, Field(max_length=150)]
    role_id: int
    email_verified: Annotated[bool, Field(default=False)]
    is_blocked: Annotated[bool, Field(default=False)]
    created_at: Annotated[datetime, Field(frozen=True)]
    updated_at: datetime
    last_login_time: datetime | None

    @field_serializer("created_at", "updated_at", "last_login_time")
    def serialize_datetime(self, dt: datetime) -> str | None:
        if dt is None:
            return None
        return dt.strftime("%Y-%m-%d %H:%M")


class UserCreateDTO(DTO):
    phone: Annotated[str, Field(max_length=20)]
    email: Annotated[str, Field(max_length=100)]
    display_name: Annotated[str, Field(max_length=150)]
    role_id: int
    email_verified: Annotated[bool, Field(default=False)]


class UserEditDTO(DTO):
    phone: Annotated[str | None, Field(max_length=20)] = None
    email: Annotated[str | None, Field(max_length=100)] = None
    display_name: Annotated[str | None, Field(max_length=150)] = None
