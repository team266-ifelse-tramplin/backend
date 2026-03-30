from datetime import datetime
from typing import Annotated, Literal

from pydantic import UUID4, Field, field_serializer

from database.dto.base import DTO


class ApplicationDTO(DTO):
    id: Annotated[UUID4, Field(frozen=True)]
    opportunity_id: Annotated[UUID4, Field(frozen=True)]
    applicant_id: Annotated[UUID4, Field(frozen=True)]
    status: Annotated[
        Literal["pending", "accepted", "rejected", "reserved"], Field(max_length=50)
    ]
    cover_letter: str | None
    applied_at: datetime
    updated_at: datetime

    @field_serializer("applied_at", "updated_at")
    def serialize_datetime(self, dt: datetime) -> str | None:
        if dt is None:
            return None
        return dt.strftime("%Y-%m-%d %H:%M")


class ApplicationCreateDTO(DTO):
    opportunity_id: Annotated[UUID4, Field(frozen=True)]
    applicant_id: Annotated[UUID4, Field(frozen=True)]
    cover_letter: str | None = None
    status: Annotated[
        Literal["pending", "accepted", "rejected", "reserved"], Field(max_length=50)
    ] = "pending"


class ApplicationEditDTO(DTO):
    status: Annotated[
        Literal["pending", "accepted", "rejected", "reserved"] | None,
        Field(max_length=50),
    ] = None
    cover_letter: str | None = None


class ApplicationsListWithQuantity(DTO):
    applications: list[ApplicationDTO]
    quantity: int
