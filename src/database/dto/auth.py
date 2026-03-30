from typing import Annotated

from pydantic import Field

from database.dto.base import DTO


class SignUpDTO(DTO):
    email: Annotated[str, Field(max_length=100)]
    phone: Annotated[str, Field(max_length=20)]
    display_name: Annotated[str, Field(max_length=150)]
    role_id: int


class SignInDTO(DTO):
    email: Annotated[str, Field(max_length=100)]
    code: Annotated[str, Field(min_length=6, max_length=6)]


class SignOutDTO(DTO):
    token: str


class SendMailcodeDTO(DTO):
    email: Annotated[str, Field(max_length=100)]
    purpose: Annotated[str, Field(max_length=20)] = "login"


class RefreshDTO(DTO):
    refresh_token: str
