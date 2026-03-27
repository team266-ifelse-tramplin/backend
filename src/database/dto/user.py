from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal

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
    created_at: datetime
    updated_at: datetime
    last_login_time: datetime | None

class UserCreateDTO(DTO):
    phone: Annotated[str, Field(max_length=20)]
    email: Annotated[str, Field(max_length=100)]
    display_name: Annotated[str, Field(max_length=150)]
    role_id: int
    email_verified: Annotated[bool, Field(default=False)]

class UserEditDTO(DTO):
    pass
