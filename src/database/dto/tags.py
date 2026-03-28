from typing import Annotated, Literal
from database.dto.base import DTO
from pydantic import Field

class TagDTO(DTO):
    name: Annotated[str, Field(max_length=100, examples=["Python"])]
    category: Annotated[
        Literal["skill", "level", "employment_type"],
        Field(examples=["skill"])
    ] = "skill"
