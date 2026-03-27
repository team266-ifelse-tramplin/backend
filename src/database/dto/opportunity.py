from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal

from fastapi import Query
from pydantic import UUID4, Field, field_serializer

from database.dto.base import DTO


class OpportunityDTO(DTO):
    id: Annotated[UUID4, Field(frozen=True)]
    title: Annotated[str, Field(max_length=255)]
    description: str
    company_id: UUID4
    opportunity_type: (
        Annotated[
            Literal["vacancy", "internship", "mentoring", "event"], Field(max_length=30)
        ]
        | None
    )
    work_format: (
        Annotated[
            Literal['office', 'hybrid', 'remote'], Field(max_length=30)
        ]
        | None
    )
    employment: Annotated[Literal["full", "partial"], Field(max_length=15)] | None
    level: (
        Annotated[Literal["intern", "junior", "middle", "senior"], Field(max_length=10)]
        | None
    )
    tags_data: list[str] | None
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
    employment: Annotated[Literal["full", "partial"], Field(max_length=15)]
    level: (
        Annotated[Literal["intern", "junior", "middle", "senior"], Field(max_length=10)]
        | None
    )
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
    status: Literal["active", "closed"] | None = Query(
        None, description="Статус возможности"
    )
    opportunity_type: Literal["vacancy", "internship", "mentoring", "event"] | None = (
        Query(None, description="Тип возможности")
    )
    work_format: Literal["office", "hybrid", "remote"] | None = Query(
        None, description="Формат работы/участия"
    )
    level: Literal["intern", "junior", "middle", "senior"] | None = Query(
        None, description="Уровень специалиста"
    )
    salary_from: int | None = Query(None, description="Минимум оплаты")
    salary_to: int | None = Query(None, description="Максимум оплаты")
    employment: str | None = Query(None, description="Полная / частичная занятость")
    location: str | None = Query(None, description="Место проведения")
