from datetime import datetime
from typing import Annotated, Literal

from fastapi import Query
from pydantic import UUID4, Field, field_serializer

from core.const import DT_EXAMPLE
from database.dto.base import DTO
from database.dto.tags import TagDTO


class OpportunityDTO(DTO):
    id: Annotated[UUID4, Field(frozen=True)]
    title: Annotated[str, Field(max_length=255)]
    description: str
    company_id: Annotated[UUID4, Field(frozen=True)]
    opportunity_type: (
        Annotated[
            Literal["vacancy", "internship", "mentoring", "event"], Field(max_length=30)
        ]
        | None
    )
    work_format: (
        Annotated[Literal["office", "hybrid", "remote"], Field(max_length=30)] | None
    )
    employment: Annotated[Literal["full", "partial"], Field(max_length=15)] | None
    level: (
        Annotated[Literal["intern", "junior", "middle", "senior"], Field(max_length=10)]
        | None
    )
    tags_data: list[TagDTO] | None
    location: Annotated[str | None, Field(max_length=255)]
    latitude: float | None  ## TODO: значения через API Яндекс.Карты стоит брать
    longitude: float | None
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
    def serialize_datetime(self, dt: datetime) -> str | None:
        if dt is None:
            return None
        return dt.strftime("%Y-%m-%d %H:%M")


class OpportunityEditDTO(DTO):
    title: Annotated[str | None, Field(max_length=255)] = None
    description: str | None = None
    opportunity_type: Annotated[
        Literal["vacancy", "internship", "mentoring", "event"] | None,
        Field(alias="type")
    ] = None
    work_format: Annotated[Literal["office", "hybrid", "remote"] | None, Field()] = None
    employment: Annotated[Literal["full", "partial"] | None, Field()] = None
    level: (
        Annotated[Literal["intern", "junior", "middle", "senior"], Field(max_length=10)]
        | None
    ) = None
    location: Annotated[str | None, Field(max_length=255)] = None
    latitude: float | None = None
    longitude: float | None = None
    salary_from: int | None = None
    salary_to: int | None = None
    currency: Annotated[str | None, Field(min_length=3, max_length=3)] = None
    publication_date: datetime | None = Field(default=None, examples=[DT_EXAMPLE])
    expiration_date: datetime | None = Field(default=None, examples=[DT_EXAMPLE])
    event_date: datetime | None = Field(default=None, examples=[DT_EXAMPLE])
    status: Annotated[str | None, Field(max_length=50)] = None

class OpportunityCreateDTO(DTO):
    title: Annotated[str, Field(max_length=255)] 
    description: str
    company_id: Annotated[UUID4, Field(frozen=True)]
    opportunity_type: (
        Annotated[
            Literal["vacancy", "internship", "mentoring", "event"], Field(max_length=30)
        ]
        | None
    )
    work_format: (
        Annotated[Literal["office", "hybrid", "remote"], Field(max_length=30)] | None
    )
    employment: Annotated[Literal["full", "partial"], Field(max_length=15)] | None
    level: (
        Annotated[Literal["intern", "junior", "middle", "senior"], Field(max_length=10)]
        | None
    )
    tags_data: list[TagDTO] | None = None
    location: Annotated[str | None, Field(max_length=255)] = None
    latitude: float | None = None  ## TODO: значения через API Яндекс.Карты стоит брать
    longitude: float | None = None
    salary_from: int | None = None
    salary_to: int | None = None
    currency: Annotated[str | None, Field(min_length=3, max_length=3)] = "RUB"
    publication_date: datetime = Field(default_factory=datetime.now, examples=[DT_EXAMPLE])
    expiration_date: datetime | None = Field(default=None, examples=[DT_EXAMPLE])
    event_date: datetime | None = Field(default=None, examples=[DT_EXAMPLE])
    contact_info: str | None = None
    status: Annotated[str, Field(max_length=50)] = "active"
    created_by: Annotated[UUID4, Field(frozen=True)] | None = None
    views_count: Annotated[int, Field(default=0)] | None = None
    created_at: Annotated[datetime, Field(frozen=True)] | None = None
    updated_at: datetime | None = None

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


class OpportunityListWithQuantityDTO(DTO):
    opportunities: list[OpportunityDTO]
    quantity: int
