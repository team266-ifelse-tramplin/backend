from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal
from base import DTO
from pydantic import UUID4, Field, field_serializer
from fastapi import Query


class OpportunityDTO(DTO):
    id: Annotated[UUID4, Field(frozen=True)]
    title: Annotated[str | None, Field(max_length=255)]
    description: str | None
    company_id: UUID4
    opportunity_type: Annotated[str, Field(max_length=30, alias="type")]
    work_format: Annotated[Literal["vacancy", "internship", "mentoring", "event"], Field(max_length=30)]
    location: Annotated[str | None, Field(max_length=255)]
    latitude: Decimal | None  ## TODO: значения через API Яндекс.Карты стоит брать
    longitude: Decimal | None
    salary_from: int | None
    salary_to: int | None
    currency: Annotated[str | None, Field(min_length=3, max_length=3)]
    publication_date: datetime
    expiration_date: datetime | None
    event_date: datetime | None
    contact_info: str | None
    status: Annotated[str, Field(max_length=50, default="active")]
    created_by: Annotated[UUID4, Field(frozen=True)]
    views_count: Annotated[int, Field(default=0)]
    created_at: Annotated[datetime, Field(frozen=True)]
    updated_at: datetime

    @field_serializer(
        "publication_date", "expiration_date", "event_date", "created_at", "updated_at"
    )
    def serialize_datetime(self, dt: datetime) -> str:
        if dt is None:
            return None
        return dt.isoformat(sep=" ", timespec="seconds")


class OpportunityEditDTO(DTO):
    title: Annotated[str | None, Field(max_length=255)]
    description: str | None
    opportunity_type: Annotated[str, Field(max_length=30, alias="type")]
    work_format: Annotated[str, Field(max_length=30)]
    location: Annotated[str | None, Field(max_length=255)]
    latitude: Decimal | None
    longitude: Decimal | None
    salary_from: int | None
    salary_to: int | None
    currency: Annotated[str | None, Field(min_length=3, max_length=3)]
    publication_date: datetime
    expiration_date: datetime | None
    event_date: datetime | None
    status: Annotated[str, Field(max_length=50, default="active")]


class OpportunityFiltersDTO(DTO):
    status: Literal["active", "closed"] | None = Query(None, description="Статус возможности")
    work_format: Literal["vacancy", "internship", "mentoring", "event"] | None = Query(None, description="Формат работы/участия")
    salary_from: int | None = Query(None, description="Минимум оплаты")
    salary_to: int | None = Query(None, description="Максимум оплаты")
    ...

    
