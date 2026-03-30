from typing import Annotated, Literal

from pydantic import Field

from database.dto.base import DTO


class TagDTO(DTO):
    name: Annotated[str, Field(max_length=100, examples=["Python"])]
    category: Annotated[
        Literal["skill", "level", "employment_type"], Field(examples=["skill"])
    ] = "skill"
