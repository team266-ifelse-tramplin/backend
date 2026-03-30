from datetime import datetime
from typing import Annotated

from pydantic import UUID4, Field, field_serializer

from database.dto.base import DTO


class FavouriteDTO(DTO):
    id: Annotated[UUID4, Field(frozen=True)]
    user_id: Annotated[UUID4, Field(frozen=True)]
    opportunity_id: Annotated[UUID4, Field(frozen=True)]
    created_at: datetime

    @field_serializer("created_at")
    def serialize_datetime(self, dt: datetime) -> str | None:
        if dt is None:
            return None
        return dt.strftime("%Y-%m-%d %H:%M")


class FavouriteAddDTO(DTO):
    user_id: Annotated[UUID4, Field(frozen=True)]
    opportunity_id: Annotated[UUID4, Field(frozen=True)]


class FavouritesListWithQuantity(DTO):
    favourites: list[FavouriteDTO]
    quantity: int
